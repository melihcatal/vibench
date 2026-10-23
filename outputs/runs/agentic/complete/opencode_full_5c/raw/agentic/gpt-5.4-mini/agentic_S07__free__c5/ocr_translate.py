from typing import Any, Dict
from google.cloud import translate_v3 as translate
from document_models import OCRRequest


def translate_ocr_text(text: str, target_language: str = 'es') -> Dict[str, Any]:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client._transport._host.split('.')[0] if hasattr(client, '_transport') else 'project'}/locations/global"
    response = client.translate_text(request={'parent': parent, 'contents': [text], 'mime_type': 'text/plain', 'target_language_code': target_language})
    return {'provider': 'google_translate_v3', 'translations': [item.translated_text for item in response.translations]}
