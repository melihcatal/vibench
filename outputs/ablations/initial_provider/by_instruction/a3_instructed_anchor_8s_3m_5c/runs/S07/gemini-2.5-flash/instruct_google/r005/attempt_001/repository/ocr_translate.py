from google.cloud import translate_v2 as translate
from document_models import ExtractedText

def translate_ocr_text(extracted_text: ExtractedText, target_language: str) -> ExtractedText:
    """Translates extracted OCR text using Google Cloud Translation API."""
    client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    translation = client.translate(
        extracted_text.text_content, target_language=target_language
    )

    return ExtractedText(text_content=translation["translatedText"])

if __name__ == "__main__":
    # Example usage: Replace with your extracted text and target language
    # extracted_text = ExtractedText(text_content="Hello World")
    # translated_text = translate_ocr_text(extracted_text, "es")
    # print(translated_text.text_content)
    pass
