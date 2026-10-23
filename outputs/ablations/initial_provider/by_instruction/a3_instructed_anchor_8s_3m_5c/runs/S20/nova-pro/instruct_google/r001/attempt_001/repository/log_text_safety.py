import re

def check_log_text_safety(log_text):
    unsafe_patterns = [r'password', r'secret', r'confidential']
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True

log_text = 'This is a log message with no unsafe content'

if check_log_text_safety(log_text):
    print('Log text is safe')
else:
    print('Log text contains unsafe content')