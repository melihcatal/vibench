from google.cloud import language_v1

def check_caption_safety(text: str) -> dict:
    """Checks live transcript text for unsafe content using Google Cloud Natural Language AI."""

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-content
    response = client.moderate_text(document=document)

    safety_scores = {}
    for category_filter in response.moderation_categories:
        safety_scores[category_filter.name] = category_filter.score

    return safety_scores
