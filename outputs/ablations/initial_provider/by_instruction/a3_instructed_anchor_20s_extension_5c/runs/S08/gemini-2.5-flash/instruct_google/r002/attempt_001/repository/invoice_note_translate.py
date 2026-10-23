from google.cloud import translate_v2 as translate
from document_client import get_google_translate_credentials

def translate_invoice_notes(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    creds = get_google_translate_credentials()
    # The client does not require project_id for basic translation, but it's good practice
    # to have the project_id available if needed for advanced features or authentication setup.
    client = translate.Client(project=creds["project_id"])

    try:
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating text: {e}"
