from google.cloud import language_v2
import os


def record_text_safety(text_content: str) -> dict:
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-text
    response = client.moderate_text(document=document)

    safety_scores = {}
    for category_filter in response.moderation_categories:
        safety_scores[category_filter.name] = category_filter.score
    return safety_scores
