from google.cloud import translate_v3
import os

def translate_appeal_text(text: str, target_language_code: str = "en", project_id: str = None) -> dict:
    """
    Translates appeal text for review using Google Cloud Translation API.

    Args:
        text: The text of the appeal to translate.
        target_language_code: The BCP-47 language code to translate the text into. Defaults to "en" (English).
        project_id: Your Google Cloud project ID. If None, it tries to get from GCP_PROJECT_ID env var.

    Returns:
        A dictionary containing the original text, translated text, and detected source language.
    """
    client = translate_v3.TranslationServiceClient()

    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    detected_source_language = "unknown"

    for translation in response.translations:
        translated_text = translation.translated_text
        detected_source_language = translation.detected_language_code
        break # Assuming only one text content

    return {
        "original_text": text,
        "translated_text": translated_text,
        "detected_source_language": detected_source_language,
        "target_language": target_language_code
    }

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") 

    if project_id == "your-gcp-project-id":
        print("WARNING: Please set the GCP_PROJECT_ID environment variable or update the script with your actual project ID.")
        print("Using a placeholder project ID, which will likely fail without proper authentication/configuration.")

    example_appeal_es = "Este contenido fue marcado injustamente. Creo que cumple con las pautas de la comunidad."
    translation_es = translate_appeal_text(example_appeal_es, target_language_code="en", project_id=project_id)
    print(f"Original (ES): {translation_es['original_text']}")
    print(f"Translated (EN): {translation_es['translated_text']}")
    print(f"Detected Source Language: {translation_es['detected_source_language']}")

    example_appeal_fr = "Je pense que la décision de modération est incorrecte."
    translation_fr = translate_appeal_text(example_appeal_fr, target_language_code="en", project_id=project_id)
    print(f"\nOriginal (FR): {translation_fr['original_text']}")
    print(f"Translated (EN): {translation_fr['translated_text']}")
    print(f"Detected Source Language: {translation_fr['detected_source_language']}")

    example_appeal_en = "This is an appeal in English."
    translation_en = translate_appeal_text(example_appeal_en, target_language_code="es", project_id=project_id)
    print(f"\nOriginal (EN): {translation_en['original_text']}")
    print(f"Translated (ES): {translation_en['translated_text']}")
    print(f"Detected Source Language: {translation_en['detected_source_language']}")
