import re


def extract_fields(text):
    fields = {}
    matches = re.finditer(r"(\w+)\s*:\s*(\w+)", text)
    for match in matches:
        fields[match.group(1)] = match.group(2)
    return fields
