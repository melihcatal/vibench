from google.cloud import language_v1
from typing import Dict, Any

def analyze_safety_of_text(text_content: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/reference/rest/v1/ModerateTextRequest
    response = client.moderate_text(document=document)

    safety_scores = {}
    for category_filter in response.moderation_categories:
        safety_scores[category_filter.name] = category_filter.score
    
    return safety_scores
