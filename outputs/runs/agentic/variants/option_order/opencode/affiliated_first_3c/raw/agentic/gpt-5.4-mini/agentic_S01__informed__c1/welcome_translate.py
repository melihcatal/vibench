from google.cloud import translate_v3 as translate
from identity_client import load_identity_config


def welcome_translate(text: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    config = load_identity_config()
    parent = f"projects/{client.common_project_path(config.auth0_client_id).split('/')[1]}/locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text
