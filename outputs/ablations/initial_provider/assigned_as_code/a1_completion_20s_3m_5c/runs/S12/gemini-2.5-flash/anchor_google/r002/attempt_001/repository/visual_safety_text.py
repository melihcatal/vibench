from google.cloud import language_v1

def check_visual_safety_text(payload, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()
    
    text_content = payload["text_content"]
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/categories
    # We'll use the moderateText method for explicit safety checks
    response = client.moderate_text(document=document)

    safety_scores = {}
    for category_mention in response.moderation_categories:
        safety_scores[category_mention.name] = category_mention.score

    return {"safety_scores": safety_scores}
