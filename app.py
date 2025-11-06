import argparse
import json
import os
import sys
from utils.web3_client import get_w3
from utils.hashing import code_hash
from config import RPC_URLS, DEFAULT_CHAIN, MANIFEST_PATH

BANNER = "🔍 EVM Contract Soundness Manifest — hash & verify"

def load_manifest(path: str):
    if not os.path.exists(path):
        print(f"❌ Manifest not found at {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def cmd_hash(args):
    chain = args.chain or DEFAULT_CHAIN
    w3 = get_w3(RPC_URLS[chain])
    if not w3.is_connected():
        print(f"❌ Failed to connect RPC for chain '{chain}'")
        sys.exit(1)
    h = code_hash(w3, args.address)
    print(f"Chain: {chain}")
    print(f"Address: {args.address}")
    print(f"Code hash: {h}")

def cmd_check(args):
    chain = args.chain or DEFAULT_CHAIN
    data = load_manifest(args.manifest)
    if chain not in data:
        print(f"❌ Chain '{chain}' not present in manifest")
        sys.exit(1)
    w3 = get_w3(RPC_URLS[chain])
    if not w3.is_connected():
        print(f"❌ Failed to connect RPC for chain '{chain}'")
        sys.exit(1)

    target = data[chain].get(args.key)
    if not target:
        print(f"❌ Key '{args.key}' not found under chain '{chain}'")
        sys.exit(1)

    addr = target["address"]
    expected = target["expected_code_hash"].lower()
    actual = code_hash(w3, addr).lower()
    status = "✅ MATCH" if expected == actual else "❌ MISMATCH"
    print(f"[{status}] {args.key} @ {addr}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")

def cmd_audit(args):
    chain = args.chain or DEFAULT_CHAIN
    data = load_manifest(args.manifest)
    if chain not in data:
        print(f"❌ Chain '{chain}' not present in manifest")
        sys.exit(1)
    w3 = get_w3(RPC_URLS[chain])
    if not w3.is_connected():
        print(f"❌ Failed to connect RPC for chain '{chain}'")
        sys.exit(1)

    failures = 0
    total = 0
    for key, entry in data[chain].items():
        total += 1
        addr = entry["address"]
        expected = entry["expected_code_hash"].lower()
        actual = code_hash(w3, addr).lower()
        ok = expected == actual
        if ok:
            print(f"✅ {key} — OK")
        else:
            print(f"❌ {key} — code hash mismatch")
            print(f"   addr: {addr}")
            print(f"   expected: {expected}")
            print(f"   actual:   {actual}")
            failures += 1

    print("\nSummary:")
    print(f"  Checked: {total}")
    print(f"  Failures: {failures}")
    print("  Result:", "✅ PASS" if failures == 0 else "❌ FAIL")

def cmd_bootstrap(args):
    """Create a manifest entry by reading the current on-chain code hash."""
    chain = args.chain or DEFAULT_CHAIN
    w3 = get_w3(RPC_URLS[chain])
    if not w3.is_connected():
        print(f"❌ Failed to connect RPC for chain '{chain}'")
        sys.exit(1)
    h = code_hash(w3, args.address).lower()
    data = {"address": args.address, "expected_code_hash": h, "notes": args.notes or ""}
    print(json.dumps({args.key: data}, indent=2))
    print("\n💡 Paste the above under the correct chain in your manifest.json")

def build_parser():
    p = argparse.ArgumentParser(description=BANNER)
    p.add_argument("--chain", choices=list(RPC_URLS.keys()), default=DEFAULT_CHAIN, help="Target chain")
    p.add_argument("--manifest", default=MANIFEST_PATH, help="Path to manifest.json")

    sub = p.add_subparsers(required=True)

    p_hash = sub.add_parser("hash", help="Print code hash for an address")
    p_hash.add_argument("address", help="0x-address to inspect")
    p_hash.set_defaults(func=cmd_hash)

    p_check = sub.add_parser("check", help="Compare one manifest entry vs on-chain code")
    p_check.add_argument("key", help="Logical key in manifest (e.g., DepositContract)")
    p_check.set_defaults(func=cmd_check)

    p_audit = sub.add_parser("audit", help="Audit all manifest entries for a chain")
    p_audit.set_defaults(func=cmd_audit)

    p_boot = sub.add_parser("bootstrap", help="Generate a manifest snippet from live code")
    p_boot.add_argument("key", help="Logical key for this contract")
    p_boot.add_argument("address", help="0x-address")
    p_boot.add_argument("--notes", help="Optional notes")
    p_boot.set_defaults(func=cmd_bootstrap)

    return p

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
