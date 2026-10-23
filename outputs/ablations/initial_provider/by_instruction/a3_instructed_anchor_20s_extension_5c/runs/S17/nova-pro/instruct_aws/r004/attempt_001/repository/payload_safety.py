import re

def check_decrypted_payload(decrypted_text):
    if re.search(r'unsafe_pattern', decrypted_text):
        return 'Unsafe content detected'
    return 'Safe content'