from web3 import Web3
from config import Config
import json
import os

class BlockchainHelper:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
        self.contract = None
        self.account = None
        self.abi = None
        
        # Load ABI if exists
        abi_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
        if os.path.exists(abi_path) and Config.CONTRACT_ADDRESS:
            with open(abi_path, 'r') as f:
                self.abi = json.load(f)
            # Use checksum address
            checksum_address = self.w3.to_checksum_address(Config.CONTRACT_ADDRESS)
            self.contract = self.w3.eth.contract(address=checksum_address, abi=self.abi)
            
            # Use the first account in Ganache as default
            if self.w3.is_connected() and len(self.w3.eth.accounts) > 0:
                self.w3.eth.default_account = self.w3.eth.accounts[0]

    def is_connected(self):
        return self.w3.is_connected()

    def create_batch_on_chain(self, public_id, batch_type, origin):
        if not self.contract:
            return None
        
        try:
            tx_hash = self.contract.functions.createBatch(
                public_id, batch_type, origin
            ).transact()
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            print(f"Blockchain error: {e}")
            return None

    def add_event_on_chain(self, public_id, event_type, timestamp_int):
        if not self.contract:
            return None
        
        try:
            tx_hash = self.contract.functions.addEvent(
                public_id, event_type, timestamp_int
            ).transact()
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            print(f"Blockchain error: {e}")
            return None

    def get_batch_info(self, public_id):
        if not self.contract:
            return None
        try:
            return self.contract.functions.batches(public_id).call()
        except Exception:
            return None

    def get_events(self, public_id):
        if not self.contract:
            return None
        try:
            return self.contract.functions.getEvents(public_id).call()
        except:
            return []
