# 🧬 Bio-Tech Supply Chain Traceability System

A lightweight, end-to-end web application for tracing biological product batches through their supply chain, with blockchain-backed immutability, strict step-by-step event sequence enforcement, AI-powered shelf-life prediction, and RAG-based preservation advice.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask + Flask-Login + Flask-SQLAlchemy |
| Database | SQLite (local) |
| Blockchain | Solidity smart contract on Ganache (local Ethereum) |
| ML | scikit-learn (Linear Regression shelf-life model) |
| RAG | sentence-transformers + NumPy cosine similarity |
| Frontend | Pico.css + custom dark theme + Vanilla JS |

---

## 📁 Project Structure

```
SupplyChainApp/
├── app.py                   # Flask application & all API routes
├── models.py                # SQLAlchemy models (User, Batch, Event, Document)
├── config.py                # App configuration (reads from .env)
├── blockchain_helper.py     # Web3.py helper for Ganache integration
├── deploy_contract.py       # Script to compile & deploy Solidity contract
├── SupplyChainTrace.sol     # Smart contract source
├── requirements.txt         # Python dependencies
├── setup.bat                # Windows one-click setup script
├── .env                     # Environment variables (SECRET_KEY, CONTRACT_ADDRESS)
│
├── ml/
│   ├── train_model.py       # Trains shelf-life predictor → saves model.pkl
│   └── model.pkl            # [Generated] Trained scikit-learn pipeline
│
├── rag/
│   ├── knowledge_base.json  # Preservation tips knowledge base
│   ├── build_kb.py          # Encodes KB → saves embeddings.npy + ids.json
│   ├── embeddings.npy       # [Generated] Sentence embeddings
│   └── ids.json             # [Generated] Entry ID mapping
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Shared nav layout
│   ├── login.html
│   ├── dashboard.html
│   ├── add_batch.html
│   ├── add_event.html
│   ├── batch_detail.html    # ML + RAG buttons, event history
│   └── chat.html            # Chatbot modal (included in dashboard)
│
└── static/
    ├── style.css            # Dark teal theme, glassmorphism cards
    └── main.js              # AJAX calls: predict, advise, chatbot
```

---

## ⚙️ Setup & Installation

### Step 1 — Clone and Setup Environment (Windows)

```bat
cd SupplyChainApp
setup.bat
```

This single script will:
1. Create a Python virtual environment (`venv/`)
2. Install all dependencies from `requirements.txt`
3. Train the ML shelf-life model → `ml/model.pkl`
4. Build RAG knowledge-base embeddings → `rag/embeddings.npy`

### Step 2 — Start Blockchain (Optional but recommended)

Download [Ganache](https://trufflesuite.com/ganache/) and start it, then:

```bat
venv\Scripts\activate
python deploy_contract.py
```

This compiles `SupplyChainTrace.sol`, deploys it to Ganache, and automatically writes the contract address to `.env`. **The app works without this step** — blockchain columns will show "Local only".

### Step 3 — Run the App

```bat
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

**Default credentials:** `admin` / `admin123`

---

## 🔑 Features

| Feature | How to Use |
|---|---|
| **Batch Registration** | Click "Register New Batch" → fill form → submit |
| **Event Logging** | Click "Log New Event" → Enforces `Collection` -> `Transport` -> `Storage` -> `Packaging` -> `Dispose` |
| **Blockchain Proof** | Batch & Event creation records a Tx hash to Ganache |
| **Visual Timeline** | Dashboard → "Track Timeline" to see a visual chain of custody |
| **Shelf-Life Prediction** | Batch Detail page → "Predict Shelf-Life (AI)" button |
| **Preservation Advice** | Batch Detail page → "Get Preservation Advice (RAG)" button |
| **AI Chatbot** | Dashboard → "Ask AI Assistant" button (Integrates with RAG + DB) |

---

## 🌐 API Endpoints

| Method | Route | Description |
|---|---|---|
| GET/POST | `/login` | Login form |
| GET | `/` | Dashboard (recent batches) |
| GET/POST | `/batches/create` | Register a new batch |
| GET | `/batches/<public_id>` | Batch detail + event history |
| GET/POST | `/events/create` | Log a new supply chain event |
| GET | `/ml/predict/<public_id>` | AI shelf-life prediction (JSON) |
| GET | `/preservation/advise/<public_id>` | RAG preservation advice (JSON) |
| POST | `/chat` | Chatbot query endpoint (JSON) |

---

## 📝 Default Login

| Username | Password | Role |
|---|---|---|
| admin | admin123 | admin |

To add more users, extend the database initialization in `app.py` or add a registration route.
