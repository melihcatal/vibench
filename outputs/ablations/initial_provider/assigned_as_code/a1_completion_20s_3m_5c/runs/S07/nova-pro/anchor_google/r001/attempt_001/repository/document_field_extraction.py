import re

def extract_fields(text):
    fields = {}
    patterns = [
        (r'Name:\s*(.+)', 'name'),
        (r'Address:\s*(.+)', 'address'),
        (r'Phone:\s*(.+)', 'phone')
    ]
    for pattern, field in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field] = match.group(1)
    return fields