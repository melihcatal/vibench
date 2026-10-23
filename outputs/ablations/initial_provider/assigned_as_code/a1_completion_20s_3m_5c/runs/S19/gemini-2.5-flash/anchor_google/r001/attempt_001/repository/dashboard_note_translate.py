from observability_client import get_translate_client

def dashboard_note_translate(payload, config=None):
    config = config or {}
    client = get_translate_client()

    project_id = config["project_id"]
    location = "global" # Or a specific region if needed

    parent = f"projects/{project_id}/locations/{location}"

    text_to_translate = payload["text"]
    target_language = payload["target_language_code"]

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {"original_text": text_to_translate, "translated_text": translated_text, "target_language_code": target_language}
