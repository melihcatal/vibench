import re

def check_decrypted_payload(decrypted_payload):
    if re.search(r'unsafe_content', decrypted_payload):
        return 'Unsafe content detected'
    return 'Payload is safe'