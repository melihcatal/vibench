import os
from google.cloud import translate_v3 as translate

def translate_invoice_note(text_content: str, target_language_code: str = "es", project_id: str = None) -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable or pass it to the function.")
        return ""

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    # Translate text from English to the target language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return " ".join(translations)

if __name__ == '__main__':
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    sample_note = "Please note, payment terms are 30 days from the invoice date."
    target_lang = "fr"

    if not PROJECT_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable and ensure Google Cloud credentials are configured.")
    else:
        print(f"Translating note to {target_lang}...")
        translated_text = translate_invoice_note(sample_note, target_language_code=target_lang, project_id=PROJECT_ID)
        print("Original:", sample_note)
        print(f"Translated ({target_lang}):", translated_text)

        sample_note_german = "Vielen Dank für Ihre Bestellung."
        target_lang_english = "en"
        print(f"\nTranslating note to {target_lang_english}...")
        translated_text_en = translate_invoice_note(sample_note_german, target_language_code=target_lang_english, project_id=PROJECT_ID)
        print("Original:", sample_note_german)
        print(f"Translated ({target_lang_english}):", translated_text_en)
