import os
from document_client import DocumentClient
from document_models import TranslatedText

def ocr_translate(text: str, target_language: str, config: dict = None) -> TranslatedText:
    config = config or {}
    project_id = config.get("GOOGLE_CLOUD_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    if not project_id:
        raise ValueError("Google Cloud project ID not provided for translation.")

    document_client_helper = DocumentClient(config)
    client = document_client_helper.get_google_translate_client()

    # The format_glossary_path method is needed to construct the parent for translation
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text_output = ""
    source_language_code = ""
    for translation in response.translations:
        translated_text_output = translation.translated_text
        source_language_code = translation.detected_language_code # Assuming all content is one language
        break

    return TranslatedText(translated_text=translated_text_output, source_language=source_language_code, target_language=target_language)
