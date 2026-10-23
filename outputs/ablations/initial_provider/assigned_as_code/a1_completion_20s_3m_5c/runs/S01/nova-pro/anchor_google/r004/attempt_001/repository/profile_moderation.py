import re


def profile_moderation(text):
    if re.search(r'\b(badword1|badword2)\b', text, re.IGNORECASE):
        return {"status": "rejected"}
    return {"status": "approved"}