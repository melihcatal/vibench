import re

def extract_fields(text):
    fields = {}
    # Example regex for field extraction
    field_pattern = re.compile(r'(\w+):\s*(\w+)')
    matches = field_pattern.finditer(text)
    for match in matches:
        fields[match.group(1)] = match.group(2)
    return fields