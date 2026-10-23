import re

def moderate_vendor_text(text: str):
    if re.search(r'\b(sensitive|confidential)\b', text, re.IGNORECASE):
        raise ValueError('Vendor text contains sensitive information')