"""
deploy_contract.py
==================
Run this script AFTER starting Ganache to compile and deploy
SupplyChainTrace.sol, then automatically write the address + ABI
into contract_abi.json and update the .env file.

Requirements:
    pip install py-solc-x web3 python-dotenv
"""

import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc

GANACHE_URL = os.environ.get('GANACHE_URL', 'http://127.0.0.1:8545')
SOL_FILE    = os.path.join(os.path.dirname(__file__), 'SupplyChainTrace.sol')
ABI_OUT     = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
ENV_FILE    = os.path.join(os.path.dirname(__file__), '.env')

def main():
    print("[1/4] Installing solc compiler (0.8.0)...")
    install_solc('0.8.0')

    print("[2/4] Compiling SupplyChainTrace.sol...")
    with open(SOL_FILE, 'r') as f:
        source = f.read()

    compiled = compile_standard({
        "language": "Solidity",
        "sources": {"SupplyChainTrace.sol": {"content": source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
            }
        }
    }, solc_version='0.8.0')

    abi      = compiled['contracts']['SupplyChainTrace.sol']['SupplyChainTrace']['abi']
    bytecode = compiled['contracts']['SupplyChainTrace.sol']['SupplyChainTrace']['evm']['bytecode']['object']

    print("[3/4] Deploying to Ganache...")
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not w3.is_connected():
        print("ERROR: Cannot connect to Ganache. Make sure it is running on", GANACHE_URL)
        return

    w3.eth.default_account = w3.eth.accounts[0]
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash  = Contract.constructor().transact({'gas': 3000000})
    receipt  = w3.eth.wait_for_transaction_receipt(tx_hash)
    address  = receipt.contractAddress

    print(f"    Contract deployed at: {address}")

    print("[4/4] Saving ABI and updating .env ...")
    with open(ABI_OUT, 'w') as f:
        json.dump(abi, f, indent=2)

    # Update .env
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()

    # Remove old CONTRACT_ADDRESS line if present
    lines = [l for l in lines if not l.startswith('CONTRACT_ADDRESS=')]
    lines.append(f"CONTRACT_ADDRESS={address}\n")

    with open(ENV_FILE, 'w') as f:
        f.writelines(lines)

    print("\nDeployment complete!")
    print(f"  ABI saved to  : {ABI_OUT}")
    print(f"  .env updated  : CONTRACT_ADDRESS={address}")
    print("\nYou can now start the Flask app:  python app.py")

if __name__ == '__main__':
    main()
