from google.cloud import translate_v3 as translate

def translate_dashboard_note(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API.

    Provider: Google Cloud Translation API
    """
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Provider-identifying signal: translate_v3.TranslationServiceClient.translate_text
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
