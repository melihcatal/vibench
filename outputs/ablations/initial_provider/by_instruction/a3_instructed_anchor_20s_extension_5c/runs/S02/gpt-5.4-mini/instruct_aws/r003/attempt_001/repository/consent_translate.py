from google.cloud import translate_v3 as translate


def translate_consent(text: str, target_language: str):
    client = translate.TranslationServiceClient()
    parent = client.common_location_path("project", "global")
    response = client.translate_text(
        request={"parent": parent, "contents": [text], "target_language_code": target_language, "mime_type": "text/plain"}
    )
    return response.translations[0].translated_text
