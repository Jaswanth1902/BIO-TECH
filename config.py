import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'supply_chain.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Blockchain Config
    GANACHE_URL = os.environ.get('GANACHE_URL') or 'http://127.0.0.1:8545'
    CONTRACT_ADDRESS = os.environ.get('CONTRACT_ADDRESS') or ''  # Will be populated after deployment
    
    # ML & RAG Config
    MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
    KB_PATH = os.path.join(BASE_DIR, 'rag', 'knowledge_base.json')
    EMBEDDINGS_PATH = os.path.join(BASE_DIR, 'rag', 'embeddings.npy')
    IDS_PATH = os.path.join(BASE_DIR, 'rag', 'ids.json')
