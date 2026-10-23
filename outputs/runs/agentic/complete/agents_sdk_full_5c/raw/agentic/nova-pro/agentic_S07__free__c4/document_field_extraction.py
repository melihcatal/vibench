import re

def extract_fields(text):
    fields = {}
    fields['name'] = re.search(r'Name: (.+)', text).group(1)
    fields['address'] = re.search(r'Address: (.+)', text).group(1)
    return fields