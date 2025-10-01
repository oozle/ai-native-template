# scripts/sign_example_receipt.py
import json, base64, os
from datetime import datetime, timezone
from nacl.signing import SigningKey

PUB_DIR = "keys"
os.makedirs(PUB_DIR, exist_ok=True)

# 1) generate keypair once (or reuse if exists)
sk_path = os.path.join(PUB_DIR, "publisher.key")
pk_path = os.path.join(PUB_DIR, "publisher.pub")
if not os.path.exists(sk_path):
    sk = SigningKey.generate()
    with open(sk_path, "wb") as f: f.write(sk._seed)
    with open(pk_path, "w") as f: f.write(sk.verify_key.encode().hex())
else:
    with open(sk_path, "rb") as f:
        sk = SigningKey(f.read())

# 2) build example receipt payload (without signature)
receipt = {
    "request_id": "req_demo_0001",
    "publisher_id": "urn:publisher:oozle.ai-native-template",
    "resource_id": "kb/article/42",
    "units": { "unit": "1k_tokens", "value": 1.7 },
    "fee_computed": 0.0017,
    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "alg": "Ed25519"
}

# 3) sign canonical JSON
msg = json.dumps(receipt, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
sig = sk.sign(msg).signature
receipt["signature"] = base64.b64encode(sig).decode("ascii")

# 4) write to examples/receipt.example.json
os.makedirs("examples", exist_ok=True)
with open("examples/receipt.example.json", "w", encoding="utf-8") as f:
    json.dump(receipt, f, indent=2, ensure_ascii=False)

print("Wrote examples/receipt.example.json and keys/publisher.pub")
