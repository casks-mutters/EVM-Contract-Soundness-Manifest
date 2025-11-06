import os

# You can override via environment variables, e.g.:
#   export RPC_MAINNET=https://mainnet.infura.io/v3/xyz
RPC_URLS = {
    "mainnet": os.getenv("RPC_MAINNET", "https://mainnet.infura.io/v3/your_api_key"),
    "sepolia": os.getenv("RPC_SEPOLIA", "https://sepolia.infura.io/v3/your_api_key"),
}

DEFAULT_CHAIN = os.getenv("DEFAULT_CHAIN", "sepolia")
MANIFEST_PATH = os.getenv("MANIFEST_PATH", "manifest.json")
