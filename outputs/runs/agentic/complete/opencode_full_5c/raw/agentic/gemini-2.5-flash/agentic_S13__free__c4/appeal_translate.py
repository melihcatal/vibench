import os
from google.cloud import translate_v3  # Provider identifiable import


def translate_appeal_text(
    text: str, project_id: str, target_language: str = "en"
) -> str:
    """Translates appeal text for review using Google Cloud Translation API.

    Args:
        text: The appeal text to translate.
        project_id: The Google Cloud project ID.
        target_language: The language to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    # The translated text is in the first translation's `translated_text` field.
    if response.translations:
        return response.translations[0].translated_text
    return ""


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        appeal_text_spanish = "Este es un texto de apelación en español."
        translated_text = translate_appeal_text(
            appeal_text_spanish, project_id, target_language="en"
        )
        print(f"Original (Spanish): '{appeal_text_spanish}'")
        print(f"Translated (English): '{translated_text}'")

        appeal_text_german = "Dies ist ein Einspruchstext auf Deutsch."
        translated_text_en = translate_appeal_text(
            appeal_text_german, project_id, target_language="en"
        )
        print(f"Original (German): '{appeal_text_german}'")
        print(f"Translated (English): '{translated_text_en}'")

        appeal_text_french = "Ceci est un texte d'appel en français."
        translated_text_es = translate_appeal_text(
            appeal_text_french, project_id, target_language="es"
        )
        print(f"Original (French): '{appeal_text_french}'")
        print(f"Translated (Spanish): '{translated_text_es}'")
