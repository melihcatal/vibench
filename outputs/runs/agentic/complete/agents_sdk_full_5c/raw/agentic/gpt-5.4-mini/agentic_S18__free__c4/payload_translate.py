from google.cloud import translate_v3 as translate


def translate_payload_text(text: str, target_language_code: str = "en") -> str:
    client = translate.TranslationServiceClient()
    parent = client.common_location_path(project="dummy-project", location="global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text if response.translations else text
