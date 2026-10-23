from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML content
            "target_language_code": target_language,
        }
    )

    translations = [translation.translated_text for translation in response.translations]
    return " ".join(translations)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    # Placeholder for OCR extracted text
    ocr_extracted_text = "Hola, mundo. Esto es una prueba."
    target_lang = "en"

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_result = translate_text(ocr_extracted_text, YOUR_PROJECT_ID, target_lang)
        print(f"Original Text: {ocr_extracted_text}")
        print(f"Translated Text ({target_lang}): {translated_result}")
