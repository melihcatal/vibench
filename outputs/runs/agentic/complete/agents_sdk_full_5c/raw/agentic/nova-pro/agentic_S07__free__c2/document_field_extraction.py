import re

def extract_fields(text):
    fields = {}
    # Example regex for extracting fields
    for match in re.finditer(r'(\w+)\s*:\s*(\w+)', text):
        fields[match.group(1)] = match.group(2)
    return fields