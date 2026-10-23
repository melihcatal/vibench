import os
from google.cloud import translate_v3 as translate
from vision_models import TranslatedText


def translate_alt_text(text: str, target_language_code: str = "en") -> TranslatedText:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    translated_text = (
        response.translations[0].translated_text if response.translations else ""
    )
    return TranslatedText(translated_text=translated_text)
