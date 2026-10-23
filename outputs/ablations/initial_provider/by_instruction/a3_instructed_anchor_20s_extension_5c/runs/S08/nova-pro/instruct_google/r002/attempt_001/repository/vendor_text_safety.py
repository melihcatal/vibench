import re

def moderate_vendor_text(text):
    moderated_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return moderated_text