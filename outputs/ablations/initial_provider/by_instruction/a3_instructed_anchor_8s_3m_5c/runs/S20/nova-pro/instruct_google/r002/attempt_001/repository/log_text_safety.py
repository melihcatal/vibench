import re

def check_log_text_safety(log_text):
    unsafe_patterns = [r'password', r'secret', r'confidential']
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True

if __name__ == '__main__':
    log_text = 'This is a log message with no unsafe content'
    print(check_log_text_safety(log_text))