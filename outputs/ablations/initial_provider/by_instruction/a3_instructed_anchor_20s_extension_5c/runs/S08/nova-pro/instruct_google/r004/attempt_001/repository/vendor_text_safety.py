import re

def moderate_vendor_text(vendor_text):
    moderated_text = re.sub(r'\b(badword1|badword2)\b', '[REDACTED]', vendor_text, flags=re.IGNORECASE)
    return moderated_text