import re


def profile_moderation(text):
    # Example moderation: remove any text containing 'badword'
    moderated_text = re.sub(r"\bbadword\b", "", text)
    return moderated_text
