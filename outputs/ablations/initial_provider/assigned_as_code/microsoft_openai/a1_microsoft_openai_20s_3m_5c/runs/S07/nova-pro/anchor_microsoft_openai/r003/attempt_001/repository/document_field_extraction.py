import re

def extract_fields(text):
    fields = {}
    # Example regex for extracting fields (to be expanded based on actual requirements)
    field_regex = re.compile(r'(\w+)\s*:\s*(\w+)')
    matches = field_regex.findall(text)
    for match in matches:
        fields[match[0]] = match[1]
    return fields