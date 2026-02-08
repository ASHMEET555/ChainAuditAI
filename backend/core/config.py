import os
from dotenv import load_dotenv

# 1. Load variables from .env file
load_dotenv()

# 2. Read variables
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = 11155111  # Sepolia

# 3. Validation - Print warnings if keys are missing
if not CONTRACT_ADDRESS:
    print("WARNING: CONTRACT_ADDRESS is missing in .env")
if not PRIVATE_KEY:
    print("WARNING: PRIVATE_KEY is missing in .env")

# 4. Other Settings
DATABASE_URL = "sqlite:///./fraud.db"
# Ensure these paths are absolute or correct relative to main.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ABI_PATH = "blockchain/abi.json"
MODEL_PATH = os.path.join(BASE_DIR, "model_wts")