
from google.cloud import translate_v3 as translate

def translate_alt_text(text: str, target_language_code: str = "en") -> str:
    """Translates alt text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    location = "global"  # Or your desired region
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    for translation in response.translations:
        return translation.translated_text
    return text

if __name__ == "__main__":
    example_text = "Una imagen de un perro feliz corriendo en un campo."
    translated_text = translate_alt_text(example_text, "en")
    print(f"Original: {example_text}")
    print(f"Translated (English): {translated_text}")

    example_text_2 = "A happy cat sitting on a couch."
    translated_text_2 = translate_alt_text(example_text_2, "es")
    print(f"Original: {example_text_2}")
    print(f"Translated (Spanish): {translated_text_2}")
