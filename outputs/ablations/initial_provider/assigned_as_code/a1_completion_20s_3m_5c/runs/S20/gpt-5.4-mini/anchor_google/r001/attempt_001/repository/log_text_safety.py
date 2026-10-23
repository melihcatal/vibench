from google.cloud import language_v1


def log_text_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "")
    response = client.classify_text(request={"document": {"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT}})
    categories = [item.name for item in response.categories]
    return {"text": text, "categories": categories, "safe": not any("Adult" in name or "Harm" in name for name in categories)}
