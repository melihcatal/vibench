import re

def moderate_vendor_text(text):
    # Example moderation: remove profanity
    profanity_pattern = re.compile(r'\b(badword1|badword2)\b', re.IGNORECASE)
    moderated_text = profanity_pattern.sub('[moderated]', text)
    return moderated_text