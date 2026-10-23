
from google.cloud import language_v1

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud Natural Language API.

    Args:
        text: The profile text to moderate.

    Returns:
        A dictionary containing moderation results.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # For content moderation, typically you'd use classify_text or analyze_sentiment
    # depending on the specific moderation criteria.
    # Here, we'll use classify_text as an example for content categorization which can
    # be used to flag inappropriate content.
    response = client.classify_text(request={"document": document})

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    # You would then apply your moderation logic based on the categories and their confidence scores.
    # For instance, flagging content if certain categories (e.g., "Violent Content") have high confidence.

    return {"moderation_categories": categories}

if __name__ == "__main__":
    profile_text_1 = "This is a normal profile description about my hobbies."
    profile_text_2 = "I enjoy offensive content and hate speech."

    print(f"Moderating text 1: {profile_text_1}")
    result_1 = moderate_profile_text(profile_text_1)
    print(f"Result 1: {result_1}")

    print(f"Moderating text 2: {profile_text_2}")
    result_2 = moderate_profile_text(profile_text_2)
    print(f"Result 2: {result_2}")
