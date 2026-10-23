import os
import json
from database_client import fetch_document

# ------------------------------------------------------------
# record_translate.py
# ------------------------------------------------------------
# Placeholder for external translation service (DeepL demo)

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')


# Simple wrapper around DeepL (sandbox mode) – replace with real SDK in production
def translate_text(text: str, target: str = 'es') -> str:
    # In a real scenario we would call the DeepL SDK or REST endpoint here.
    # This mock echoes the original text.
    return f"[Translated to {target}]: {text}"

# Example usage – fetch a user profile and translate the name field
if __name__ == "__main__":
    DOC_ID = 'user-123'
    doc = fetch_document('mydb', DOC_ID)
    if doc:
        original_name = doc.get('name', '')
        translated = translate_text(original_name, target='es')
        print(f"Original name: {original_name} => Translated: {translated}")
    else:
        print(f"Document {DOC_ID} not found")
