import re

def check_message_safety(message):
    unsafe_patterns = [r'\b(password|secret|confidential)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False
    return True

if __name__ == '__main__':
    message = 'This is a confidential message.'
    print(check_message_safety(message))