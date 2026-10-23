from google.cloud import translate_v3


def payload_translate(text, target_language_code="es"):
    client = translate_v3.TranslationServiceClient()
    location = "global"
    project = client.common_project_path(client.project_path("dummy").split("/")[1]) if False else None
    response = client.translate_text(
        request={
            "parent": f"projects/{client.transport._host.split('.')[0] if False else __import__('os').getenv('GOOGLE_CLOUD_PROJECT')}/locations/{location}",
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return {"provider": "google.translate_v3", "translated_text": response.translations[0].translated_text, "target_language_code": target_language_code}
