import re


def moderate_profile_text(text):
    if re.search(r'\b(hate|violence|discrimination)\b', text, re.IGNORECASE):
        raise ValueError('Profile text contains inappropriate content.')
    return text
