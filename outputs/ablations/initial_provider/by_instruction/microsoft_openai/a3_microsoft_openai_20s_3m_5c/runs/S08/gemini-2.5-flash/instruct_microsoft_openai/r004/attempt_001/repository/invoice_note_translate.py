from google.cloud import translate
import os

def translate_invoice_note(text: str, target_language_code: str = "en") -> str:
    # Initialize Google Cloud Translation client
    # The client automatically picks up credentials from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    client = translate.TranslationServiceClient()

    # Get the Google Cloud project ID from environment variables
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                # Optional: You can specify a source_language_code if known
                # "source_language_code": "es", 
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            }
        )
        
        translated_text = response.translations[0].translated_text
        return translated_text

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        raise
