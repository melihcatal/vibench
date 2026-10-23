from google.cloud import language_v2

def moderate_text(text_content: str):
    """
    Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Available categories for content analysis can be found in the API documentation.
    # For a comprehensive list, refer to:
    # https://cloud.google.com/natural-language/docs/reference/rest/v2/ContentCategory
    response = client.analyze_content(
        document=document,
        # You can specify categories to analyze, or leave it empty for default.
        # categories=["toxicity", "sexual", "violence"]
    )

    return response.moderate_text_detection.moderation_categories
