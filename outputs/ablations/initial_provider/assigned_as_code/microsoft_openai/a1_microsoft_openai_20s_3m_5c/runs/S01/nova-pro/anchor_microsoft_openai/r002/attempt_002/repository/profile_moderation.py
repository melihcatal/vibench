import re


def moderate_profile_text(text):
    if re.search(r'\b(badword1|badword2)\b', text, re.IGNORECASE):
        raise ValueError('Profile text contains inappropriate content')
    return text
