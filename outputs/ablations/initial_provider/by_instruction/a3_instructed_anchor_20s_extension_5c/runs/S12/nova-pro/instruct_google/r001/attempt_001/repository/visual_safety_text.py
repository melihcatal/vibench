import re

def check_unsafe_text(text):
    unsafe_patterns = [r'\b(expletive|offensive)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

if __name__ == '__main__':
    labels = ['sample', 'labels']
    for label in labels:
        if check_unsafe_text(label):
            print(f'Unsafe label detected: {label}')