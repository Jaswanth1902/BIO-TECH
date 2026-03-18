from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User, Batch, Event
from blockchain_helper import BlockchainHelper
from datetime import datetime
import os
import pickle
import numpy as np

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

b_helper = BlockchainHelper()

# Initialize DB
with app.app_context():
    db.create_all()
    # Create default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@login_required
def dashboard():
    batches = Batch.query.order_by(Batch.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', batches=batches)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/batches/create', methods=['GET', 'POST'])
@login_required
def create_batch():
    if request.method == 'POST':
        public_id = request.form['public_id']
        batch_type = request.form['batch_type']
        name = request.form['name']
        origin = request.form['origin']
        
        if Batch.query.filter_by(public_id=public_id).first():
            flash('Batch ID already exists!', 'error')
            return redirect(url_for('create_batch'))
            
        # Create in Blockchain
        tx_hash = b_helper.create_batch_on_chain(public_id, batch_type, origin)
        
        # Save to Local DB
        batch = Batch(public_id=public_id, batch_type=batch_type, name=name, origin=origin, blockchain_tx_hash=tx_hash)
        db.session.add(batch)
        db.session.commit()
        
        if tx_hash:
            flash(f'Batch created and recorded on blockchain (Tx: {tx_hash[:10]}...)', 'success')
        else:
            flash('Batch created locally, but blockchain connection failed.', 'warning')
            
        return redirect(url_for('dashboard'))
        
    return render_template('add_batch.html')

@app.route('/batches/<public_id>')
@login_required
def batch_detail(public_id):
    batch = Batch.query.filter_by(public_id=public_id).first_or_404()
    events = batch.events.order_by(Event.timestamp.desc()).all()
    
    # Optional blockchain verification
    chain_events = b_helper.get_events(public_id) if b_helper.is_connected() else []
    
    return render_template('batch_detail.html', batch=batch, events=events, chain_events=chain_events)

@app.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    batches = Batch.query.all()
    
    batch_states = {}
    for b in batches:
        latest = b.events.order_by(Event.timestamp.desc()).first()
        batch_states[b.id] = latest.event_type if latest else None

    if request.method == 'POST':
        batch_id = request.form['batch_id']
        event_type = request.form['event_type']
        location = request.form['location']
        temperature = request.form.get('temperature', type=float)
        humidity = request.form.get('humidity', type=float)
        remarks = request.form['remarks']
        
        batch = Batch.query.get(batch_id)
        if not batch:
            flash('Invalid Batch selected.', 'error')
            return redirect(url_for('create_event'))
            
        current_state = batch_states.get(batch.id)
        allowed_events = []
        if not current_state: allowed_events = ['collection']
        elif current_state == 'collection': allowed_events = ['transport']
        elif current_state == 'transport': allowed_events = ['storage']
        elif current_state == 'storage': allowed_events = ['package']
        elif current_state == 'package': allowed_events = ['dispose']
        
        if event_type not in allowed_events:
            flash(f"Invalid sequence! Cannot log '{event_type}' after '{current_state}'.", 'error')
            return redirect(url_for('create_event'))
            
        timestamp_int = int(datetime.utcnow().timestamp())
        
        tx_hash = b_helper.add_event_on_chain(batch.public_id, event_type, timestamp_int)
        
        event = Event(
            batch_id=batch.id, event_type=event_type, location=location,
            temperature=temperature, humidity=humidity, remarks=remarks,
            blockchain_tx_hash=tx_hash
        )
        db.session.add(event)
        db.session.commit()
        
        flash('Event successfully recorded in sequence.', 'success')
        return redirect(url_for('batch_detail', public_id=batch.public_id))
        
    return render_template('add_event.html', batches=batches, batch_states=batch_states)

@app.route('/ml/predict/<public_id>')
@login_required
def predict_shelf_life(public_id):
    batch = Batch.query.filter_by(public_id=public_id).first_or_404()
    
    # Load model
    if not os.path.exists(app.config['MODEL_PATH']):
        return jsonify({'error': 'Model not trained yet.'}), 404
        
    # Gather recent events data
    events = batch.events.all()
    if not events:
        return jsonify({'error': 'Not enough data to predict.', 'remaining_days': 'N/A', 'risk_label': 'Unknown'})
        
    temps = [e.temperature for e in events if e.temperature is not None]
    hums = [e.humidity for e in events if e.humidity is not None]
    
    avg_temp = sum(temps) / len(temps) if temps else 25.0
    max_temp = max(temps) if temps else 25.0
    avg_hum = sum(hums) / len(hums) if hums else 60.0
    
    elapsed_days = (datetime.utcnow() - batch.created_at).days
    
    try:
        with open(app.config['MODEL_PATH'], 'rb') as f:
            model = pickle.load(f)
            
        import pandas as pd
        pt_encoded = 1 if batch.batch_type == 'food' else 0
        features = pd.DataFrame(
            [[avg_temp, max_temp, avg_hum, elapsed_days, pt_encoded]],
            columns=['avg_temp', 'max_temp', 'avg_humidity', 'elapsed_days', 'product_type']
        )
        prediction = model.predict(features)[0]
        
        rem_days = int(round(prediction))
        
        if rem_days > 7:
            risk = "Safe"
        elif rem_days > 2:
            risk = "At Risk"
        else:
            risk = "Critical"
            
        return jsonify({'remaining_days': rem_days, 'risk_label': risk})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preservation/advise/<public_id>')
@login_required
def advise_preservation(public_id):
    batch = Batch.query.filter_by(public_id=public_id).first_or_404()
    
    try:
        import json
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        
        if not os.path.exists(app.config['EMBEDDINGS_PATH']):
            return jsonify({'error': 'RAG Knowledge base not built.'}), 404
            
        # Mock Context collection
        query = f"preserve {batch.batch_type} {batch.name} produced in {batch.origin}"
        
        # In an actual deployment, you preload this model on startup
        model = SentenceTransformer('all-MiniLM-L6-v2')
        q_emb = model.encode([query])
        
        kb_embs = np.load(app.config['EMBEDDINGS_PATH'])
        with open(app.config['IDS_PATH'], 'r') as f:
            ids = json.load(f)
            
        similarities = cosine_similarity(q_emb, kb_embs)[0]
        best_idx = np.argmax(similarities)
        best_match_id = ids[best_idx]
        
        with open(app.config['KB_PATH'], 'r') as f:
            kb = json.load(f)
            
        best_entry = next((item for item in kb if item["id"] == best_match_id), None)
        
        return jsonify({
            'advice': best_entry['text'] if best_entry else "No specific advice found.",
            'confidence': float(similarities[best_idx])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/timeline')
@login_required
def timeline():
    batches = Batch.query.order_by(Batch.created_at.desc()).all()
    return render_template('timeline.html', batches=batches, current_batch=None)

@app.route('/timeline/<public_id>')
@login_required
def timeline_batch(public_id):
    batches = Batch.query.order_by(Batch.created_at.desc()).all()
    batch = Batch.query.filter_by(public_id=public_id).first_or_404()
    events = batch.events.order_by(Event.timestamp.asc()).all()
    
    stages = ['collection', 'transport', 'storage', 'package', 'dispose']
    completed_events = {e.event_type: e for e in events}
    
    current_stage_idx = 0
    for i, s in enumerate(stages):
        if s in completed_events:
            current_stage_idx = i + 1
            
    if current_stage_idx >= len(stages):
        current_stage_idx = len(stages) - 1
        if 'dispose' in completed_events:
            current_stage_idx = 5
            
    return render_template('timeline.html', 
                           batches=batches, 
                           current_batch=batch,
                           events=completed_events,
                           current_stage_idx=current_stage_idx,
                           stages=stages)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    question = data.get('question', '').lower().strip()
    
    # 1. Greetings & Help
    if question in ['hello', 'hi', 'hey', 'start']:
        return jsonify({"answer": "Hello! I can answer questions about preservation, check your recent batches, or guide you. What do you need?"})
    
    if 'what can u do' in question or 'what can you do' in question or 'help' in question or 'useful' in question:
        return jsonify({"answer": "I am an intelligent traceability assistant! I can search our RAG knowledge base to advise you on how to store specific products (e.g., 'how to store milk' or 'herb preservation'), or check system stats like 'how many batches do we have?'."})
    
    # 2. Database Queries
    if 'batch' in question or 'batches' in question:
        count = Batch.query.count()
        recent = Batch.query.order_by(Batch.created_at.desc()).first()
        ans = f"We currently are tracking {count} batches in the system."
        if recent:
            ans += f" The latest is {recent.name} (ID: {recent.public_id})."
        return jsonify({"answer": ans})
        
    # 3. RAG Knowledge Base Search Fallback
    try:
        import json
        import numpy as np
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        
        if os.path.exists(app.config['EMBEDDINGS_PATH']):
            model = SentenceTransformer('all-MiniLM-L6-v2')
            q_emb = model.encode([question])
            kb_embs = np.load(app.config['EMBEDDINGS_PATH'])
            
            with open(app.config['IDS_PATH'], 'r') as f:
                ids = json.load(f)
                
            similarities = cosine_similarity(q_emb, kb_embs)[0]
            best_idx = np.argmax(similarities)
            
            # Provide RAG answer if it's somewhat relevant
            if similarities[best_idx] > 0.15:
                best_match_id = ids[best_idx]
                with open(app.config['KB_PATH'], 'r') as f:
                    kb = json.load(f)
                best_entry = next((item for item in kb if item["id"] == best_match_id), None)
                if best_entry:
                    return jsonify({"answer": f"Based on our knowledge base: {best_entry['text']}"})
    except Exception as e:
        print(f"Chatbot RAG Error: {e}")
    
    return jsonify({"answer": "I'm a bit unsure about that. Try asking me how to preserve specific items like herbs or bio-samples, or ask about your 'recent batches'."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
