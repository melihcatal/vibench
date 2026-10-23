from google.cloud import translate
import os


def translate_alt_text(text, target_language_code, project_id=None):
    client = translate.TranslationServiceClient()

    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    return translations
