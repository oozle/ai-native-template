# packages/receipt-verifier-py/verify.py
import json, base64, sys
from nacl.signing import VerifyKey

def verify_receipt(receipt_path, pubkey_path):
    with open(receipt_path, "r", encoding="utf-8") as f:
        receipt = json.load(f)
    with open(pubkey_path, "r", encoding="utf-8") as f:
        pub_hex = f.read().strip()

    sig_b64 = receipt.pop("signature")
    msg = json.dumps(receipt, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    sig = base64.b64decode(sig_b64)
    VerifyKey(bytes.fromhex(pub_hex)).verify(msg, sig)
    return True

if __name__ == "__main__":
    try:
        ok = verify_receipt(sys.argv[1], sys.argv[2])
        print("VALID" if ok else "INVALID")
    except Exception as e:
        print(f"INVALID: {e}")
        sys.exit(1)
