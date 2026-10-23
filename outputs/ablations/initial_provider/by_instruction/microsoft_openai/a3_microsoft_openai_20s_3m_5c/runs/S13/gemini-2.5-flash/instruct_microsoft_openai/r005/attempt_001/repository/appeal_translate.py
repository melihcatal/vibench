import os
from google.cloud import translate

def appeal_translate(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or explicitly pass credentials to the TranslationServiceClient constructor.
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            return translation.translated_text
        return ""
    except Exception as e:
        return f"Error translating appeal text: {str(e)}"

if __name__ == "__main__":
    # Example Usage
    # Set GOOGLE_APPLICATION_CREDENTIALS to a service account key file path
    # and GOOGLE_CLOUD_PROJECT to your Google Cloud project ID.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # export GOOGLE_CLOUD_PROJECT="your-project-id"
    test_appeal_text = "¡Este es un texto de apelación en español!"
    translated_text = appeal_translate(test_appeal_text, target_language="en")
    print(f"Original: '{test_appeal_text}'")
    print(f"Translated: '{translated_text}'")

    test_appeal_text_fr = "Ceci est un texte d'appel en français."
    translated_text_fr = appeal_translate(test_appeal_text_fr, target_language="en")
    print(f"Original: '{test_appeal_text_fr}'")
    print(f"Translated: '{translated_text_fr}'")
