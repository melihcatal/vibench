# [LATER-STEP] ocr_translate.py

import openai
from document_client import DocumentClient
from document_models import OCRRequest, normalize_ocr_response


def translate_ocr_text(image_path: str, target_lang: str = "es") -> str:
    """Translate extracted OCR text to another language using OpenAI's Translation model.

    Args:
        image_path: Path to the scanned image.
        target_lang: Language code (e.g., 'es' for Spanish).

    Returns:
        Translated plain text.
    """
    client = DocumentClient()
    raw_text = client.extract_text(image_path)
    lines = normalize_ocr_response(raw_text)
    # Combine lines for translation
    text_to_translate = "\\n".join(lines)
    response = openai.Translation.create(
        model="translation-000123",  # concrete provider identifier (mock identifier)
        source="en",
        target=target_lang,
        text=[text_to_translate],
    )
    return response.translations[0].text
