import os
from google.cloud import translate_v3 as translate

def translate_ocr_text(text: str, target_language_code: str = "en") -> str:
    """
    Translates extracted OCR text using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = translate.TranslationServiceClient()
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCLOUD_PROJECT"))
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT or GCLOUD_PROJECT environment variable.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = [translation.translated_text for translation in response.translations]
    return " ".join(translations)

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS set)
    # text_to_translate = "Hola mundo. Esto es una prueba de traducción."
    # translated_text = translate_ocr_text(text_to_translate, "es")
    # print(f"Original: {text_to_translate}")
    # print(f"Translated (English): {translated_text}")
    pass
