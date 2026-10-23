from google.cloud import language_v1

def check_caption_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classifying text can help identify content that might be unsafe.
    # The categories returned can indicate potential issues.
    response = client.classify_text(request={'document': document})

    safety_analysis = []
    for category in response.categories:
        safety_analysis.append({
            "name": category.name,
            "confidence": category.confidence,
        })

    return {"safety_analysis": safety_analysis}
