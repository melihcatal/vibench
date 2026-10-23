import re

def check_safety(text):
    if re.search(r'[^a-zA-Z0-9\s]', text):
        return False
    return True

if __name__ == '__main__':
    print(check_safety('Hello World!'))