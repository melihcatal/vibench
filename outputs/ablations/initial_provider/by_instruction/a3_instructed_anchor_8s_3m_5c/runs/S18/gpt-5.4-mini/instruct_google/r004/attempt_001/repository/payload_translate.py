from google.cloud import translate_v3 as translate

from messaging_models import IntegrationResponse


def translate_payload(project_id: str, location: str, text: str, target_language_code: str):
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language_code, parent=parent)
    translated = response.translations[0].translated_text if response.translations else text
    return IntegrationResponse(provider="google_cloud_translate", resource=parent, details={"translated_text": translated, "target_language_code": target_language_code})
