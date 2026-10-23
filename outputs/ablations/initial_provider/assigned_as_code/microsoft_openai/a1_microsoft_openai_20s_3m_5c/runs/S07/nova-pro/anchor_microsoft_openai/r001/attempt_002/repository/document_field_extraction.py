import re

def extract_structured_fields(text):
    fields = {}
    fields['name'] = re.search(r'Name: (.+)', text)
    fields['address'] = re.search(r'Address: (.+)', text)
    fields['phone'] = re.search(r'Phone: (.+)', text)
    return {k: v.group(1) if v else None for k, v in fields.items()}