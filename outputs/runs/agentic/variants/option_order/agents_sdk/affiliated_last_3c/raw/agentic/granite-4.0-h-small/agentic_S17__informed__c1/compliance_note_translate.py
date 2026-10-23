# compliance_note_translate.py
import os
from google.cloud import translate_v2 as translate
from security_models import SignRequest, SignResponse

def translate_compliance_note(note: str, target_lang: str = 'es') -> str:
    """Translates an encryption/compliance note into the requested target language using Google Cloud Translation.

    Args:
        note (str): Original note in any language.
        target_lang (str): ISO language code (default 'es' for Spanish).

    Returns:
        str: Translated note.
    """
    client = translate.Client()
    result = client.translate(note, target_language=target_lang)
    return result['translatedText']

# Example usage (uncomment to test)
# if __name__ == '__main__':
#     orig = "The key must be rotated every 90 days according to regulatory policy."
#     print(translate_compliance_note(orig))
