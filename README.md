# EVM Contract Soundness Manifest

## Overview
A tiny, multi-file utility that computes on-chain **bytecode hashes** and compares them against a local **manifest.json**.  
It helps you detect code drift and verify “soundness” of deployed EVM contracts across networks.

> Inspired by security practices used in ecosystems like **Aztec**, **Zama (FHEVM)**, and broader **Soundness** verification ideas.  
> This repo is a generic EVM helper — no private keys, no writes, read-only RPC.

## Features
- `hash` — print the keccak256 hash of a contract’s deployed bytecode
- `check` — compare a single manifest entry vs live chain
- `audit` — verify all entries for a chain in one go
- `bootstrap` — generate a manifest snippet from the current live code

## Project Structure
- `app.py` — CLI commands and argument parsing  
- `config.py` — RPC URLs, default chain, manifest path  
- `utils/web3_client.py` — Web3 client factory  
- `utils/hashing.py` — bytecode hashing helper  
- `manifest.json` — per-chain addresses and expected hashes  
- `requirements.txt` — dependencies  
- `.gitignore` — housekeeping

## Installation
1. Python 3.10+
2. Install dependencies:
   pip install -r requirements.txt
3. Configure RPCs via env (optional):
   export RPC_SEPOLIA="https://sepolia.infura.io/v3/your_api_key"
   export RPC_MAINNET="https://mainnet.infura.io/v3/your_api_key"

## Usage
- Get a code hash:
   python app.py --chain sepolia hash 0xYourContractAddress
- Bootstrap a manifest entry:
   python app.py --chain sepolia bootstrap MyContract 0xYourContractAddress --notes "initial snapshot"
  Copy the JSON snippet into `manifest.json` under the proper chain key.
- Check a single entry:
   python app.py --chain sepolia check MyContract
- Audit a chain:
   python app.py --chain sepolia audit

## Expected Output
- `hash` — prints the chain, address, and the computed `Code hash: 0x…`
- `check` — shows ✅ MATCH or ❌ MISMATCH and both expected/actual hashes
- `audit` — iterates entries and prints a PASS/FAIL summary

## Notes
- `manifest.json` entries are keyed by a logical name (`MyContract`) with fields:
  - `address` (checksum 0x…)
  - `expected_code_hash` (0x…)
  - `notes` (free text)
- For reproducible CI, pin RPC providers and cache `manifest.json` in your repo.
- To extend:
  - Add ABI diffing, bytecode metadata parsing, or source verification (Sourcify/Etherscan).
  - Emit SARIF/JSON for CI annotations.
