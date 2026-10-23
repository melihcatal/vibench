from google.cloud import translate_v3

from identity_models import normalize_locale, normalize_text, response_payload


def welcome_translate(text: str, target_locale: str):
    client = translate_v3.TranslationServiceClient()
    project_id = client.common_project_path("dummy")
    location = "global"
    response = client.translate_text(
        request={
            "parent": f"projects/dummy/locations/{location}",
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "source_language_code": "en",
            "target_language_code": normalize_locale(target_locale),
        }
    )
    translated = (
        response.translations[0].translated_text if response.translations else ""
    )
    return response_payload(
        {
            "provider": "Google Cloud Translation",
            "target_locale": target_locale,
            "translated_text": translated,
        }
    )
