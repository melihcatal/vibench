import re

def check_decrypted_payload(payload):
    if re.search(b"unsafe", payload):
        return {"status": "unsafe"}
    return {"status": "safe"}