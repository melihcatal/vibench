from google.cloud import translate
from identity_client import get_google_cloud_config

def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> str:
    gcp_config = get_google_cloud_config()
    project_id = gcp_config["PROJECT_ID"]

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{gcp_config["LOCATION"]}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
