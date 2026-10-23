import re

def check_decrypted_payload(plaintext):
    if re.search(r'unsafe_content', plaintext):
        return 'Unsafe content detected'
    return 'Safe content'
