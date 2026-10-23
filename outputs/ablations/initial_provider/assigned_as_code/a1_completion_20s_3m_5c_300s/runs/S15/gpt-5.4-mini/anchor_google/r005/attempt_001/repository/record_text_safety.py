from google.cloud import language_v1


def record_text_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "")
    response = client.moderate_text(request={"document": {"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT}})
    return {"safe": not bool(response.moderation_categories), "categories": [c.name for c in response.moderation_categories]}
