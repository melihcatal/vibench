# [LATER-STEP] ocr_translate.py

import os
from document_client import DocumentClient
from document_models import OcrResult, normalize_ocr_response


def translate_extracted_text(source_text: str, target_lang: str) -> str:
    """Translate extracted plain text using a concrete Translation provider.

    Args:
        source_text: Plain text extracted from OCR/lay.
        target_lang: Target language code (e.g., "es", "fr").

    Returns:
        Translated text string.
    """
    # Choose Azure AI Translator as the concrete translation service (could swap any other provider)
    client = DocumentClient(service="azure_ai_translator")
    translated = client.translate(source_text=source_text, target_lang=target_lang)
    return translated


def translate_image(image_path: str, target_lang: str) -> str:
    """Extract plain text from an image then translate it.

    Args:
        image_path: Path to scanned document image.
        target_lang: Target language code.

    Returns:
        Plain translated text.
    """
    # Use Mindee as the OCR provider (replaceable)
    client = DocumentClient(service="mindee")
    raw_ocr = client.ocr(image_path=image_path)
    # Normalize to our OcrResult envelope
    norm = normalize_ocr_response(provider="mindee", raw_response=raw_ocr)
    extracted = norm.text  # fallback to .text field
    if not extracted:
        raise ValueError("OCR returned no text.")
    return translate_extracted_text(source_text=extracted, target_lang=target_lang)


def main():
    img = "sample_document.jpg"
    tgt = "es"  # Spanish
    translated = translate_image(img, tgt)
    print("Translated Text:")
    print(translated)


if __name__ == "__main__":
    main()
