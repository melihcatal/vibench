from google.cloud import translate_v3 as translate
from document_models import OCRTextResponse


def translate_ocr_text(ocr_response: OCRTextResponse, target_language_code: str, parent: str) -> str:
    client = translate.TranslationServiceClient()
    result = client.translate_text(
        request={
            "parent": parent,
            "contents": [ocr_response.text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return result.translations[0].translated_text if result.translations else ""
