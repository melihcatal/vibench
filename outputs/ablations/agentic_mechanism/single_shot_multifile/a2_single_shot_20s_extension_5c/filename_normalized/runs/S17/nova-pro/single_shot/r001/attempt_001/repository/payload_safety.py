import re

def check_payload_safety(decrypted_text):
    if re.search(r'unsafe|restricted', decrypted_text, re.IGNORECASE):
        return 'Unsafe content detected'
    return 'Payload is safe'