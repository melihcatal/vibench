from google.cloud import translate
import os

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates encryption or compliance notes for reviewers using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code to translate the text to (e.g., "fr" for French).
        project_id: The ID of the Google Cloud project.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, we'll take the first one.
    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    
    # Example usage:
    # compliance_note = "This encryption key is rotated monthly to meet PCI DSS requirements."
    # target_lang = "es" # Spanish

    # try:
    #     translated_note = translate_text(compliance_note, target_lang, project_id)
    #     print(f"Original (English): {compliance_note}")
    #     print(f"Translated ({target_lang}): {translated_note}")
    # except Exception as e:
    #     print(f"Error translating compliance note: {e}")
    #     print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud, and GOOGLE_CLOUD_PROJECT is set.")

    # compliance_note_fr = "La clé de chiffrement est mise à jour trimestriellement conformément aux directives de l'UE sur la protection des données."
    # target_lang_en = "en"
    # try:
    #     translated_note_en = translate_text(compliance_note_fr, target_lang_en, project_id)
    #     print(f"\nOriginal (French): {compliance_note_fr}")
    #     print(f"Translated ({target_lang_en}): {translated_note_en}")
    # except Exception as e:
    #     print(f"Error translating compliance note: {e}")
