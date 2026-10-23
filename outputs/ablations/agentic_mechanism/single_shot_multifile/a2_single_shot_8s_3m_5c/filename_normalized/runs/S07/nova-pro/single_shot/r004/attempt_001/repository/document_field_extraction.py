import re

def extract_fields(text):
    fields = {}
    for line in text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()
    return fields