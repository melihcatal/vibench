import os
from google.cloud import language_v2 as language


class ModerationResult:
    def __init__(
        self, is_flagged: bool, score: float, magnitude: float, detail: str = ""
    ):
        self.is_flagged = is_flagged
        self.score = score
        self.magnitude = magnitude
        self.detail = detail


def moderate_profile_text(
    text_content: str, project_id: str | None = None
) -> ModerationResult:
    # Google Cloud Natural Language API client initialization
    # The client will automatically pick up credentials from the environment
    language_client = language.LanguageServiceClient(
        project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    )

    document = language.Document(
        content=text_content, type_=language.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment for basic moderation. A highly negative sentiment might indicate inappropriate content.
    # For more robust moderation, specialized APIs like Google Cloud Content Safety or Perspective API would be used.
    response = language_LanguageServiceClient.analyze_sentiment(
        language_client, document=document
    )
    sentiment = response.document_sentiment

    is_flagged = False
    detail = ""

    # Thresholds for flagging. These are illustrative and should be tuned.
    if (
        sentiment.score < -0.5 and sentiment.magnitude > 1.0
    ):  # Very negative sentiment with high magnitude
        is_flagged = True
        detail = "Potentially inappropriate content detected due to strong negative sentiment."
    elif (
        sentiment.magnitude > 2.0
    ):  # High magnitude regardless of score, could indicate strong emotions
        is_flagged = True
        detail = "High emotional intensity detected, review recommended."

    return ModerationResult(
        is_flagged=is_flagged,
        score=sentiment.score,
        magnitude=sentiment.magnitude,
        detail=detail,
    )
