from document_client import get_translation_client
from document_models import TranslatedText
from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language_code: str, source_language_code: str = None) -> TranslatedText:
    client = get_translation_client()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code if source_language_code else None,
        }
    )

    translated_content = ""
    detected_language_code = None
    if response.translations:
        translated_content = response.translations[0].translated_text
        detected_language_code = response.translations[0].detected_language_code

    return TranslatedText(translated_content=translated_content, detected_language_code=detected_language_code)
