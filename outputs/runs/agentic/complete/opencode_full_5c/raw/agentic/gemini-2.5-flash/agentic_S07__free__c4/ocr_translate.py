from google.cloud import translate_v3beta1 as translate
from document_client import get_translate_client
from document_models import ExtractedText, TranslatedText

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "global"


def translate_ocr_text(
    text: ExtractedText, target_language_code: str = "es"
) -> TranslatedText:
    client = get_translate_client()

    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text.text],
            "target_language_code": target_language_code,
        }
    )

    translated_text_result = response.translations[0]
    return TranslatedText(
        translated_text=translated_text_result.translated_text,
        source_language=translated_text_result.detected_language_code,
        target_language=target_language_code,
    )
