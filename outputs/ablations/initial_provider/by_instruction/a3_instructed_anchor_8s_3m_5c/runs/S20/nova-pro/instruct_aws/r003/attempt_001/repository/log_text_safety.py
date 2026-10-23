import re

def check_log_text_safety(log_text):
    unsafe_patterns = [r'password', r'secret', r'sensitive']
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True

if __name__ == '__main__':
    print(check_log_text_safety('This is a safe log message.'))
    print(check_log_text_safety('This log message contains a password.'))
