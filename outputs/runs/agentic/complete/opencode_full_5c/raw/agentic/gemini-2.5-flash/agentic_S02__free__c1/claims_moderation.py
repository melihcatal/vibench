import os
from google.cloud import language_v2  # Google Cloud Natural Language API SDK
from google.cloud.language_v2 import Document, Document, AnnotateTextRequest
from identity_models import ModerationRequest, ModerationResponse


def moderate_claims(request: ModerationRequest) -> ModerationResponse:
    client = language_v2.LanguageServiceClient()

    document = Document(
        content=request.text_content,
        type_=Document.Type.PLAIN_TEXT,
        language_code=request.language_code,
    )

    # Google Cloud Natural Language API for content moderation
    # By requesting 'classify_text', we can get categories which can indicate content safety.
    # For more direct content moderation, other Google Cloud services (like Video Intelligence API for video)
    # or custom solutions might be used in conjunction.
    response = client.annotate_text(
        request={
            "document": document,
            "features": {"classify_text": True, "moderate_text": True},
        }
    )

    moderated_content = (
        response.text_content_with_offsets.text_content
    )  # This will contain the original text with potential moderation applied or notes
    is_safe = True
    categories = []

    # Google Cloud Natural Language API provides sentiment, entity, syntax, etc.
    # For explicit content moderation categories, 'moderate_text' feature is used.
    # If the moderation score for any category is high, we might consider it unsafe.
    # The exact threshold for 'safe' would depend on application requirements.
    if response.moderation_categories:
        for category in response.moderation_categories:
            categories.append(category.name)
            # A simplified check for safety: if any category has a score above a threshold, consider it unsafe.
            # The specific interpretation of scores might vary.
            if category.score > 0.7:  # Example threshold
                is_safe = False

    # Google Cloud Natural Language SDK import: google.cloud.language_v2
    return ModerationResponse(
        moderated_content=moderated_content, is_safe=is_safe, categories=categories
    )


if __name__ == "__main__":
    # To run this example, ensure you have authenticated your Google Cloud SDK
    # (e.g., `gcloud auth application-default login`).
    # Also, ensure 'google-cloud-language' is installed: pip install google-cloud-language

    test_requests = [
        ModerationRequest(text_content="This is a perfectly fine comment."),
        ModerationRequest(
            text_content="I hate you, you are terrible!", language_code="en"
        ),
        ModerationRequest(text_content="What a wonderful day!", language_code="en"),
    ]

    for i, req in enumerate(test_requests):
        print(f"\n--- Moderation Request {i + 1} ---")
        print(f"Original Text: {req.text_content}")
        try:
            response = moderate_claims(req)
            print(f"Moderated Text: {response.moderated_content}")
            print(f"Is Safe: {response.is_safe}")
            print(f"Categories: {', '.join(response.categories)}")
        except Exception as e:
            print(f"Error moderating claims: {e}")
            print(
                "Please ensure 'google-cloud-language' is installed and you are authenticated to Google Cloud."
            )
