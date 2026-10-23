import re

def extract_fields(text):
    fields = {}
    # Example regex for extracting fields
    fields['name'] = re.search(r'Name: (.+)', text).group(1) if re.search(r'Name: (.+)', text) else None
    fields['address'] = re.search(r'Address: (.+)', text).group(1) if re.search(r'Address: (.+)', text) else None
    return fields