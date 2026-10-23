from google.cloud import language_v1


def check_safety(text: str) -> Dict[str, object]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    categories = [{"name": item.name, "confidence": item.confidence} for item in response.moderation_categories]
    return {"provider": "google-cloud-language", "safe": not categories, "categories": categories}


if __name__ == "__main__":
    check_safety("example")
