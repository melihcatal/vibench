import re


def moderate_vendor_notes(notes):
    # Example moderation: remove inappropriate words
    inappropriate_words = ['badword1', 'badword2']
    for word in inappropriate_words:
        notes = re.sub(word, '[moderated]', notes, flags=re.IGNORECASE)
    return notes