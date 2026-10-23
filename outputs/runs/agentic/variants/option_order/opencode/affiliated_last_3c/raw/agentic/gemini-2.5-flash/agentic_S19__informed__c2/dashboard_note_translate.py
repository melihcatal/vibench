import os
from google.cloud import translate


def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = "".join(
        [translation.translated_text for translation in response.translations]
    )
    return translated_text


# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID are set)
# if __name__ == "__main__":
#     project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
#     note_to_translate = "The CPU utilization is abnormally high, investigate immediately."
#     target_lang = "es"
#     translated_note = translate_text(note_to_translate, target_lang, project_id)
#     print(f"Original: {note_to_translate}")
#     print(f"Translated ({target_lang}): {translated_note}")
