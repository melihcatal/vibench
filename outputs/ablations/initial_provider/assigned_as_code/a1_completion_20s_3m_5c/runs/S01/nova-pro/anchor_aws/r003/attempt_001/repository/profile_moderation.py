import re


def profile_moderation(text):
    if re.search(r'\b(badword1|badword2)\b', text, re.IGNORECASE):
        return {'status': 'rejected', 'reason': 'Contains inappropriate content'}
    return {'status': 'approved'}