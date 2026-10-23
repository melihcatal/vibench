import os
from google.cloud import translate_v3 as translate

def translate_appeal_text(text: str, target_language: str, project_id: str) -> str:
    """Translates appeal text for review using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    # Assuming a single text input, return the first translation
    return response.translations[0].translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and text)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    appeal_text = "Este es un texto de apelación en español."
    translated_text = translate_appeal_text(appeal_text, "en", project_id)
    print(f"Original: {appeal_text}")
    print(f"Translated: {translated_text}")
