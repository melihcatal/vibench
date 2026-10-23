from google.cloud import translate_v2 as translate
import os

def translate_runbook_notes(text: str, target_language: str, project_id: str) -> dict:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    """
    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        result = client.translate(text, target_language=target_language)
        return {
            "original_text": result['input'],
            "translated_text": result['translatedText'],
            "source_language": result['detectedSourceLanguage'],
            "target_language": target_language
        }
    except Exception as e:
        raise RuntimeError(f"Failed to translate runbook notes with Google Cloud Translation: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and project_id)
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS before running
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    # if project_id:
    #     notes = "The secret must be rotated every 90 days."
    #     translation = translate_runbook_notes(notes, "es", project_id)
    #     print(f"Original: {translation['original_text']}")
    #     print(f"Translated: {translation['translated_text']}")
    pass
