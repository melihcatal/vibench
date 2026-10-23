from google.cloud import translate_v3 as translate


def live_caption_translate(text: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project_path.split('/')[1]}/locations/global" if hasattr(client, "project_path") else "projects/unknown/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
