import re


def extract_fields(text):
    fields = {}
    # Example regex to extract fields (this should be more sophisticated in a real implementation)
    for match in re.finditer(r'(\w+):\s*(\w+)', text):
        fields[match.group(1)] = match.group(2)
    return fields