def payload_safety(decrypted_text):
    unsafe_content = ['malicious', 'dangerous']
    for content in unsafe_content:
        if content in decrypted_text:
            return False
    return True