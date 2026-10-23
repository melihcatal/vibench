from speech_client import get_translate_client

def translate_transcript(payload: dict, config: dict = None):
    config = config or {}
    client, parent = get_translate_client(project_id=config["project_id"], location=config.get("location", "global"))
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "source_language_code": payload["source_language_code"],
            "target_language_code": payload["target_language_code"],
        }
    )
    
    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    return {"translations": translations}
