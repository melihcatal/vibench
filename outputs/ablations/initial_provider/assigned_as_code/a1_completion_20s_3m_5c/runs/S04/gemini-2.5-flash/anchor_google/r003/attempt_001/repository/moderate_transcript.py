from google.cloud import language_v1

def moderate_transcript(text_content: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    
    moderation_categories = []
    for category in response.moderation_categories:
        moderation_categories.append({
            "name": category.name,
            "confidence": category.confidence,
        })

    return {
        "text_content": text_content,
        "moderation_categories": moderation_categories,
    }
