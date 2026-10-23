
import os
from google.cloud import translate

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates generated image descriptions using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Or infer from GOOGLE_APPLICATION_CREDENTIALS
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")
        
    location = "global"  # Or your desired region for translation

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    if response.translations:
        return response.translations[0].translated_text
    return text # Return original if no translation found

if __name__ == '__main__':
    # This is example usage.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT_ID are set.
    english_description = "A serene landscape with mountains and a clear lake."
    
    try:
        spanish_description = translate_alt_text(english_description, target_language="es")
        print(f"English: {english_description}")
        print(f"Spanish: {spanish_description}")
    except Exception as e:
        print(f"An error occurred: {e}")
