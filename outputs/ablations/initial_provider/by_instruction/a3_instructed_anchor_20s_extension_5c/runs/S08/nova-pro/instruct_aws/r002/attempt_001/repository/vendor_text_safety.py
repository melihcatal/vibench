import re

def moderate_vendor_text(vendor_text):
    moderated_text = re.sub(r'[^a-zA-Z0-9\s]', '', vendor_text)
    return moderated_text