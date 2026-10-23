
import os
from google.cloud import translate_v3 as translate

def translate_dashboard_note(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.

    Args:
        text (str): The text to translate.
        target_language_code (str): The BCP-47 language code to translate to (e.g., "es" for Spanish).
        project_id (str): Your Google Cloud project ID.

    Returns:
        str: The translated text, or an error message if translation fails.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return "No translation found."

    except Exception as e:
        return f"Error during translation: {e}"

if __name__ == "__main__":
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    text_to_translate = "CPU Utilization for Production Servers"
    target_lang = "es" # Spanish

    translated_text = translate_dashboard_note(text_to_translate, target_lang, project_id)
    print(f"Original text: '{text_to_translate}'")
    print(f"Translated to {target_lang}: '{translated_text}'")

    text_to_translate_jp = "Memory Usage by Service"
    target_lang_jp = "ja" # Japanese
    translated_text_jp = translate_dashboard_note(text_to_translate_jp, target_lang_jp, project_id)
    print(f"\nOriginal text: '{text_to_translate_jp}'")
    print(f"Translated to {target_lang_jp}: '{translated_text_jp}'")
