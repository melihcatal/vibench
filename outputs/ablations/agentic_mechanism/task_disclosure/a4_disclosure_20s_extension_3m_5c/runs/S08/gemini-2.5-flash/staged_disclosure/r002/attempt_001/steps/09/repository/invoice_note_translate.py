
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
    
    # Example usage
    invoice_note = "This is a test invoice note for translation."
    target_lang = "es"  # Translate to Spanish

    translated_note = translate_text(invoice_note, target_lang, project_id)
    print(f"Original: {invoice_note}")
    print(f"Translated ({target_lang}): {translated_note}")
