from google.cloud import translate_v2 as translate
import os

def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or gcloud auth)
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/service-account-key.json'
    english_notes = """
    Important steps for database secret rotation:
    1. Generate a new password in the vault.
    2. Update application configuration files.
    3. Restart database-dependent services.
    4. Verify connectivity.
    """
    
    print("Original English notes:")
    print(english_notes)

    print("
Translating to Spanish...")
    try:
        spanish_notes = translate_runbook_notes(english_notes, target_language="es")
        print("Translated Spanish notes:")
        print(spanish_notes)
    except Exception:
        print("Failed to translate runbook notes.")

    print("
Translating to German...")
    try:
        german_notes = translate_runbook_notes(english_notes, target_language="de")
        print("Translated German notes:")
        print(german_notes)
    except Exception:
        print("Failed to translate runbook notes.")
