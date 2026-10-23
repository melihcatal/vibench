from google.cloud import language_v1


def visual_safety_text(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=" ".join(payload.get("labels", [])), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={"document": document})
    return {"categories": [{"name": item.name, "confidence": item.confidence} for item in response.categories]}
