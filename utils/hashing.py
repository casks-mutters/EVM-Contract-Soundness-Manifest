from web3 import Web3

def code_hash(w3: Web3, address: str) -> str:
    checksum = Web3.to_checksum_address(address)
    code = w3.eth.get_code(checksum)
    return Web3.keccak(code).hex()
