import os
from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.Client(project=project_id)

    # Google Cloud Translation API identifies as 'google.cloud.translate_v2'
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with actual project ID and desired translation)
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS environment variable set
    # or authenticate otherwise for Google Cloud.
    
    # You would typically get these from a configuration or command line arguments
    # For demonstration purposes, we'll use placeholders.
    _project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-google-cloud-project-id")
    _target_language = "es"  # Example: Spanish
    _note_to_translate = "This is a dashboard note about user engagement."

    if _project_id == "your-google-cloud-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-google-cloud-project-id' with your actual Google Cloud Project ID.")
    else:
        print(f"Translating: '{_note_to_translate}' to '{_target_language}'")
        translated_text = translate_note(_note_to_translate, _target_language, _project_id)
        print(f"Translated text: {translated_text}")
