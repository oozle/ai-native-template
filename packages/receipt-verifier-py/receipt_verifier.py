from nacl.signing import VerifyKey
import base64, json

def verify_receipt(receipt: dict, public_key_hex: str) -> bool:
    data = receipt.copy()
    sig_b64 = data.pop("signature")
    msg = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode()
    sig = base64.b64decode(sig_b64)
    pub = VerifyKey(bytes.fromhex(public_key_hex))
    try:
        pub.verify(msg, sig)
        return True
    except Exception:
        return False
