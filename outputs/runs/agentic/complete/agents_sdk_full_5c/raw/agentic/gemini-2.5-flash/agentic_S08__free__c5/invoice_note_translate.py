import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate
from document_client import load_config

def translate_invoice_note(text: str, target_language_code: str = 'en') -> Dict[str, Any]:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    config = load_config("translation")
    project_id = config.get("project_id")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set for Translation.")

    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, but we're expecting a single note here.
    try:
        result = translate_client.translate(text, target_language=target_language_code)
        return {
            "original_text": text,
            "translated_text": result['translatedText'],
            "source_language": result['detectedSourceLanguage'],
            "target_language": target_language_code,
            "model": "Google Cloud Translation v2"
        }
    except Exception as e:
        return {"error": str(e), "original_text": text, "target_language": target_language_code}

if __name__ == '__main__':
    os.environ["GOOGLE_CLOUD_PROJECT_ID"] = "your-gcp-project-id"
    # Set GOOGLE_APPLICATION_CREDENTIALS for authentication

    # Example usage
    invoice_note_es = "Gracias por su negocio. Esperamos verte pronto."
    translation_result_es = translate_invoice_note(invoice_note_es, "en")
    print("Spanish Note Translation:", translation_result_es)

    print("\n"+"-"*30+"\n")

    invoice_note_fr = "Paiement dû dans les 30 jours."
    translation_result_fr = translate_invoice_note(invoice_note_fr, "en")
    print("French Note Translation:", translation_result_fr)

    print("\n"+"-"*30+"\n")

    invoice_note_en = "Thank you for your business."
    translation_result_en = translate_invoice_note(invoice_note_en, "es")
    print("English Note Translation to Spanish:", translation_result_en)

    print("To run, ensure GOOGLE_CLOUD_PROJECT_ID environment variable is set and Google Cloud authentication is configured.")
