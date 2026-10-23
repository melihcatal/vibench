from observability_client import get_language_client
from observability_models import SafetyCheckRequest, SafetyCheckResponse
from google.cloud.language_v2 import Document, DocumentSentiment, AnnotateTextRequest

def log_text_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    client = get_language_client()

    document = Document(content=request.text_content, type_=Document.Type.PLAIN_TEXT)

    # Using annotate_text for content moderation capabilities, specifically for categories
    # Note: Google Cloud Natural Language API doesn't have a direct 'safety check' API like Perspective API.
    # For a direct safety check, you'd typically use Perspective API or similar.
    # Here, we'll simulate a basic safety check by looking for negative sentiment or specific categories.
    # This is a simplified example and might not cover all aspects of 'unsafe content'.
    response = client.classify_text(document=document)

    is_safe = True
    reasons = []

    # This is a very basic example. Real-world safety checks are more complex.
    # For demonstration, let's assume if certain categories are detected, it might be unsafe.
    # This part would need significant refinement for actual content safety.
    unsafe_categories = ["/Violence", "/Hate Speech", "/Sexual Content"]
    for category in response.categories:
        if category.name in unsafe_categories and category.confidence > 0.5:
            is_safe = False
            reasons.append(f"Content classified under potentially unsafe category: {category.name}")

    # A more robust solution would involve sentiment analysis combined with keyword matching or a dedicated moderation API.

    return SafetyCheckResponse(is_safe=is_safe, reasons=reasons)
