import re

def check_log_text_safety(log_text: str) -> bool:
    unsafe_patterns = [r'password', r'secret']
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True

if __name__ == '__main__':
    log_text = 'This is a log message with no unsafe content'
    is_safe = check_log_text_safety(log_text)
    print(f'Is log text safe? {is_safe}')