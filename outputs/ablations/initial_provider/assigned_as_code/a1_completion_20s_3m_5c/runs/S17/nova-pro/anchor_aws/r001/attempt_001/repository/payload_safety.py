import re



def check_decrypted_payload(plaintext: str) -> bool:
    unsafe_patterns = [r'<script>', r'<iframe>', r'<object>', r'<embed>']
    for pattern in unsafe_patterns:
        if re.search(pattern, plaintext):
            return False
    return True
