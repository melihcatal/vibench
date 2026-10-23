import os
from google.cloud import translate_v3 as translate
from typing import Optional

def translate_invoice_note(text: str, target_language_code: str, project_id: Optional[str] = None) -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    # The source language will be automatically detected if not specified.
    # For better performance and accuracy, you can explicitly set source_language_code.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            # "source_language_code": "en", # Optional: specify source language
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
    
    return translated_text

if __name__ == "__main__":
    # Example usage
    invoice_note_english = "Thank you for your prompt payment. We appreciate your business."
    invoice_note_spanish = "Gracias por su pronto pago. Agradecemos su negocio."

    TARGET_LANGUAGE = "es" # Spanish
    # To run this example, ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # and GOOGLE_CLOUD_PROJECT environment variable is set.

    # translated_note = translate_invoice_note(invoice_note_english, TARGET_LANGUAGE)
    # print(f"English to {TARGET_LANGUAGE}: {translated_note}")

    # translated_note_back = translate_invoice_note(translated_note, "en") # Translate back to English
    # print(f"{TARGET_LANGUAGE} to English: {translated_note_back}")

    # translated_note_from_spanish = translate_invoice_note(invoice_note_spanish, "fr") # Translate Spanish to French
    # print(f"Spanish to French: {translated_note_from_spanish}")
