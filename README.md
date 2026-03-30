# 🧬 Bio-Tech Supply Chain Traceability System

A premium, end-to-end biological product tracker featuring **Blockchain-backed Immutability**, **Adaptive AI Shelf-Life Prediction**, and **RAG-powered Preservation Intelligence**.

---

## 🎯 Core Objectives & Solutions

### A. Blockchain Traceability & Compliance
**Solution:** Every lifecycle event (Collection → Transport → Storage → Packaging → Disposal) is recorded as a unique transaction on the Ethereum blockchain (Ganache).
- **Immutable Audit Trail:** Prevents tampering with temperature/humidity logs.
- **Who Tracks:** Each participant (farmers, transporters, lab techs) is responsible for their specific stage, ensuring a reliable "chain of custody."

### B. Role-Based Access Control (RBAC) 👥
**Solution:** A hierarchical permission system separates operational duties:
- **Admin:** Full system control.
- **Producer:** Authorized for **Batch Registration** and **Event Logging**.
- **Staff:** Authorized for **Analytical Monitoring** (AI Prediction, RAG Advice) but cannot modify the record.

### C. Shelf-Life Prediction & Risk Assessment 🤖
**Solution:** A custom Linear Regression ML model predicts the **Remaining Usable Window** based on dynamic environmental conditions.
- **Dynamic Risk:** If a batch is exposed to abnormal temperatures, the AI alert level shifts in real-time.

### D. Cold Chain Integrity & Compliance Reporting 📜
**Solution:** Automated validation against biological stability thresholds.
- **Integrity Status:** Instantly flags "Fail" if temperature excursions occur.
- **Official Reports:** Generates a professional, printable **Audit Certificate** with on-chain proof hashes.

### E. AI-Driven Preservation (RAG) 📚
**Solution:** A Retrieval-Augmented Generation system provides drug-specific expert guidelines (e.g., mRNA vaccine storage vs monoclonal antibody handling).

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| **Web Framework** | Flask (Python) + Flask-SQLAlchemy |
| **Blockchain** | Solidity Smart Contract + Web3.py + Ganache |
| **AI (ML/RAG)** | Scikit-learn + Sentence-Transformers |
| **Aesthetics** | Glassmorphism UI + CSS Custom Properties |

---

## 🔑 Default Accounts (RBAC)

| Role | Username | Password |
|---|---|---|
| **Admin** | `admin` | `admin123` |
| **Producer** | `producer1` | `producer123` |
| **Staff** | `staff1` | `staff123` |

---

## ⚙️ Quick Start (Windows)

1. **Setup Environment:**
   ```bat
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
2. **Build Knowledge Base:**
   ```bat
   python rag/build_kb.py
   python ml/train_model.py
   ```

3. **Start Blockchain (Optional):**
   Open [Ganache](https://trufflesuite.com/ganache/), then run:
   ```bat
   python deploy_contract.py
   ```

4. **Run Application:**
   ```bat
   python app.py
   ```
   Access at: **http://127.0.0.1:5000**

---

## 🛡️ Key Features

- **Sequential Event Enforcement:** Batches must follow clinical/safe movement steps.
- **Visual Visual Journey:** Modern horizontal/vertical timeline for every Batch.
- **Intelligent Assistant:** Chat with the AI for preservation advice or system statistics.
- **Premium Aesthetics:** Cyber-lab dark theme designed for modern biotech environments.
