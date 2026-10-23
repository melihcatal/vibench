from google.cloud import translate_v2 as translate


def ocr_translate(extracted_text, target="en"):
    """Translate extracted OCR text to a target language using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(extracted_text, target_language=target)
    return result["translatedText"]
