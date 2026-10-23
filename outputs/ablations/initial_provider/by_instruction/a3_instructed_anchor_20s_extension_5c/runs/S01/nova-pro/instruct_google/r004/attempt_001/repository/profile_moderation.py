import re

def moderate_profile_text(text):
    # Example moderation: remove profanity
    profanity_pattern = re.compile(r'\b(badword1|badword2|badword3)\b', re.IGNORECASE)
    moderated_text = profanity_pattern.sub('[profanity removed]', text)
    return moderated_text