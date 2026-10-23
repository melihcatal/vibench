
from google.cloud import translate_v2 as translate

def translate_text(text, project_id, target_language='en'):
    """Translates text into the target language using Google Cloud Translation API."""
    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Replace 'your-project-id' with your Google Cloud Project ID
    # Replace 'Hello, world!' with the actual invoice note or description
    project_id = "your-project-id"
    invoice_note = "Hola, mundo!"
    translated_note = translate_text(invoice_note, project_id, target_language="en")
    print(f"Original note: {invoice_note}")
    print(f"Translated note: {translated_note}")
