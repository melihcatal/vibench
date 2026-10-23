from security_client import get_translator_client
from azure.ai.translation.text.models import InputTextItem

def translate_compliance_note(note_text, target_language="es", source_language="en"):
    translator_client = get_translator_client()

    # The TextTranslationClient expects a list of InputTextItem
    request_body = [
        InputTextItem(text=note_text)
    ]

    # Perform the translation
    response = translator_client.translate(content=request_body, to=[target_language], from_language=source_language)

    translated_text = None
    if response and len(response) > 0:
        for translation in response[0].translations:
            translated_text = translation.text
            break # Assuming we only need the first translation

    return {
        'original_text': note_text,
        'source_language': source_language,
        'target_language': target_language,
        'translated_text': translated_text
    }
