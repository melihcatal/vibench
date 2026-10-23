import re


def moderate_vendor_notes(notes):
    # Example: Remove any notes containing 'confidential' or 'sensitive'
    moderated_notes = [note for note in notes if not re.search(r'\b(confidential|sensitive)\b', note, re.IGNORECASE)]
    return moderated_notes