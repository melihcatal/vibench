from google.cloud import translate_v3 as translate

from document_models import OCRRequest, OCRResponse, normalize_text
from extract_text import extract_text


def ocr_translate(request: OCRRequest, target_language_code: str) -> OCRResponse:
    source = extract_text(request)
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.common_project_path.split('/')[1]}" if hasattr(client, "common_project_path") else ""
    response = client.translate_text(contents=[source.text], target_language_code=target_language_code, parent=parent or "")
    translated = normalize_text(response.translations[0].translated_text if response.translations else source.text)
    return OCRResponse(text=translated, raw={"provider": "google_translate_v3", "source": source.raw})
