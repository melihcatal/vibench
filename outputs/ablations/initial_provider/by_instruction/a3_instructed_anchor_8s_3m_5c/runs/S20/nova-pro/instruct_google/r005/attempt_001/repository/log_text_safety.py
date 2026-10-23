import re

def check_log_text(log_text):
    unsafe_patterns = [
        r'password',
        r'secret',
        r'confidential'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return True
    return False

if __name__ == '__main__':
    log_text = 'This is a log message with no unsafe content'
    if check_log_text(log_text):
        print('Unsafe content detected')
    else:
        print('No unsafe content detected')