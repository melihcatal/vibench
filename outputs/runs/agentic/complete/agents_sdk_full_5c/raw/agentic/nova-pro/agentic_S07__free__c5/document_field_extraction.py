import re

def extract_fields(text):
    fields = {}
    # Example pattern for extracting key-value pairs
    pattern = re.compile(r'(\w+):\s*(\w+)')
    matches = pattern.finditer(text)
    for match in matches:
        fields[match.group(1)] = match.group(2)
    return fields