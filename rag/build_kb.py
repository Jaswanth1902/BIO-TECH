import json
import numpy as np
import os
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Please install sentence-transformers: pip install sentence-transformers")
    exit(1)

def build_kb():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.join(base_dir, 'knowledge_base.json')
    
    if not os.path.exists(kb_path):
        print(f"Error: {kb_path} not found.")
        return
        
    with open(kb_path, 'r') as f:
        kb = json.load(f)
        
    texts = [item['text'] for item in kb]
    ids = [item['id'] for item in kb]
    
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Encoding texts...")
    embeddings = model.encode(texts)
    
    emb_path = os.path.join(base_dir, 'embeddings.npy')
    ids_path = os.path.join(base_dir, 'ids.json')
    
    np.save(emb_path, embeddings)
    with open(ids_path, 'w') as f:
        json.dump(ids, f)
        
    print(f"Successfully generated and saved embeddings for {len(kb)} entries.")

if __name__ == '__main__':
    build_kb()
