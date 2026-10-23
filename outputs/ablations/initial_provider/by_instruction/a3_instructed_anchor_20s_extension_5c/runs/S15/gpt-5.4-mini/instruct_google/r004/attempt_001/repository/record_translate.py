from google.cloud import translate_v3 as translate


def translate_record(text, target_language_code, project_id, location="global"):
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(request={"parent": parent, "contents": [text], "target_language_code": target_language_code, "mime_type": "text/plain"})
    return {"translated_text": response.translations[0].translated_text if response.translations else ""}
