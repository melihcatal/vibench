import os
import json
from database_client import fetch_document

# ------------------------------------------------------------
# record_text_safety.py
# ------------------------------------------------------------
# Placeholder for external text‑safety service (Perspective API demo)

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')


# Very simple sandboxed safety check – in production replace with a real API call
def check_text_safety(text: str) -> str:
    # Here we just strip obvious profanity; real implementation would call Perspective API
    offensive_words = {'badword', 'inappropriate'}
    cleaned = ' '.join(word for word in text.split() if word.lower() not in offensive_words)
    return cleaned

# Example usage – fetch a document and run safety check
if __name__ == "__main__":
    DOC_ID = 'user-123'
    doc = fetch_document('mydb', DOC_ID)
    if doc:
        original = doc.get('description', '')
        cleaned = check_text_safety(original)
        print(f"Original: {original} => Cleaned: {cleaned}")
    else:
        print(f"Document {DOC_ID} not found")
