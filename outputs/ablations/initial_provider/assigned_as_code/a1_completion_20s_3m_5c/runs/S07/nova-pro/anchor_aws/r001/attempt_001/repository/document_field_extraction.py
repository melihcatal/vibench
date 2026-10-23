import re


def extract_fields(text):
    fields = {}
    for line in text.split('\n'):
        match = re.match(r'(\w+):\s*(.*)', line)
        if match:
            key, value = match.groups()
            fields[key] = value.strip()
    return fields