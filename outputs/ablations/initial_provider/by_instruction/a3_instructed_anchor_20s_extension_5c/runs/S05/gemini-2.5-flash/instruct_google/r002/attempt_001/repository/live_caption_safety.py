from google.cloud import language_v1


def check_for_unsafe_content(text: str):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-content
    response = client.moderate_text(document=document)

    unsafe_categories = []
    for category_filter in response.moderation_categories:
        # The score is a confidence score from 0 to 1. Higher scores indicate higher confidence.
        # A threshold of 0.7 is commonly used for flagging content.
        if category_filter.score > 0.7:
            unsafe_categories.append(
                f"{category_filter.name} (score: {category_filter.score:.2f})")

    return unsafe_categories
