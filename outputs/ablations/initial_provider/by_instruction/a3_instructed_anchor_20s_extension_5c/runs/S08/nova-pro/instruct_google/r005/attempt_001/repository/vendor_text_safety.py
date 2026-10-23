import re

def moderate_vendor_text(text):
    moderated_text = re.sub(r'[^\w\s]', '', text)
    return moderated_text