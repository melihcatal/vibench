from vision_client import VisionClient
from google.cloud import language_v1


def check_text_safety(text_content):
    client = VisionClient().language_client
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories for content classification
    # https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={"document": document})

    safety_scores = {}
    for category in response.categories:
        safety_scores[category.name] = category.confidence

    # You would typically define what constitutes "unsafe" based on confidence scores and categories
    # This is a basic example and might need more sophisticated logic
    is_unsafe = False
    unsafe_categories_found = []

    # Example: Mark as unsafe if confidence in certain categories is high
    # Note: Google Natural Language API does not directly provide 'safety' scores like Vision AI.
    # It provides content classification. We're interpreting high confidence in certain categories
    # as an indicator of "safety concern" for this task.

    # For a more direct "safety" check on text, other services or custom models might be more appropriate.
    # Here, we are using content classification as a proxy.

    # Example categories that might indicate safety concerns (this is a simplified example)
    potential_unsafe_keywords = ["/Adult", "/Gambling", "/Hate Speech", "/Violence"]

    for category in response.categories:
        if (
            category.name in potential_unsafe_keywords and category.confidence > 0.7
        ):  # High confidence
            is_unsafe = True
            unsafe_categories_found.append(category.name)

    return {
        "text_content": text_content,
        "classification_results": safety_scores,
        "is_unsafe": is_unsafe,
        "unsafe_categories_identified": unsafe_categories_found,
    }
