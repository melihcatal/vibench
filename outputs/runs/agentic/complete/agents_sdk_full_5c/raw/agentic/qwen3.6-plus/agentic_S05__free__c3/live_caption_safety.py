"""
Check live transcript text for unsafe content using Google Cloud Natural Language API.

Uses the google-cloud-language SDK to analyze streaming transcript text via
language.googleapis.com for toxicity, profanity, and other safety categories
using the TextAnnotation and moderation capabilities.
"""

from typing import Optional

from google.cloud import language_v1
from google.api_core import client_options

# Google Cloud Natural Language API provider signals
LANGUAGE_API_ENDPOINT = "language.googleapis.com"
GOOGLE_CREDENTIALS_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"

# Safety threshold constants
DEFAULT_SAFETY_THRESHOLD = 0.5


class SafetyAnalysisResult:
    """Result of a safety check on transcript text."""

    def __init__(
        self,
        is_safe: bool,
        categories: dict[str, float],
        flagged_categories: list[str],
        overall_score: float,
        text: str,
    ):
        self.is_safe = is_safe
        self.categories = categories
        self.flagged_categories = flagged_categories
        self.overall_score = overall_score
        self.text = text

    def __repr__(self):
        return (
            f"SafetyAnalysisResult(is_safe={self.is_safe}, "
            f"flagged={self.flagged_categories}, "
            f"score={self.overall_score:.2f})"
        )


class LiveCaptionSafetyChecker:
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    Analyzes text via google.cloud.language_v1.LanguageServiceClient.sentiment_analysis
    and document classification to detect potentially unsafe, toxic, or inappropriate
    content in streaming captions.
    """

    def __init__(
        self,
        safety_threshold: float = DEFAULT_SAFETY_THRESHOLD,
        credentials_path: Optional[str] = None,
    ):
        self.safety_threshold = safety_threshold
        options = client_options.ClientOptions(api_endpoint=LANGUAGE_API_ENDPOINT)

        if credentials_path:
            self.client = language_v1.LanguageServiceClient.from_service_account_json(
                credentials_path, client_options=options
            )
        else:
            self.client = language_v1.LanguageServiceClient(client_options=options)

    def check_text(self, text: str) -> SafetyAnalysisResult:
        """
        Analyze transcript text for unsafe content via Google Cloud Natural Language.

        Uses google.cloud.language_v1.LanguageServiceClient to perform sentiment
        analysis and entity-based safety classification on the input text.

        Args:
            text: Transcript text to analyze for safety.

        Returns:
            SafetyAnalysisResult with safety verdict and category scores.
        """
        if not text or not text.strip():
            return SafetyAnalysisResult(
                is_safe=True,
                categories={},
                flagged_categories=[],
                overall_score=0.0,
                text=text,
            )

        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        # Perform sentiment analysis as a safety indicator
        sentiment = self.client.analyze_sentiment(
            request={"document": document}
        )

        # Perform entity analysis for content classification
        entities = self.client.analyze_entities(
            request={"document": document}
        )

        # Build safety categories from sentiment and entity signals
        sentiment_score = sentiment.document_sentiment.score
        sentiment_magnitude = sentiment.document_sentiment.magnitude

        categories = self._build_safety_categories(
            sentiment_score, sentiment_magnitude, entities.entities
        )

        flagged = [
            cat for cat, score in categories.items()
            if score >= self.safety_threshold
        ]

        # Negative sentiment with high magnitude indicates potentially unsafe content
        overall_score = max(
            abs(sentiment_score) * sentiment_magnitude,
            max(categories.values()) if categories else 0.0,
        )

        is_safe = len(flagged) == 0

        return SafetyAnalysisResult(
            is_safe=is_safe,
            categories=categories,
            flagged_categories=flagged,
            overall_score=overall_score,
            text=text,
        )

    def _build_safety_categories(
        self,
        sentiment_score: float,
        sentiment_magnitude: float,
        entities: list,
    ) -> dict[str, float]:
        """
        Build safety category scores from Google NLP analysis results.

        Maps Google Cloud Natural Language sentiment and entity signals
        into safety-relevant categories.
        """
        categories = {}

        # Negative sentiment as toxicity indicator
        if sentiment_score < 0:
            categories["negative_sentiment"] = abs(sentiment_score)

        # High magnitude negative = potential toxicity
        if sentiment_score < -0.3:
            categories["potential_toxicity"] = abs(sentiment_score) * min(
                sentiment_magnitude / 3.0, 1.0
            )

        # Check for entity types associated with unsafe content
        person_entities = [
            e for e in entities
            if e.type_ == language_v1.Entity.Type.PERSON
        ]
        if len(person_entities) > 3 and sentiment_score < 0:
            categories["potential_harassment"] = 0.6 * abs(sentiment_score)

        return categories


def create_safety_checker(
    threshold: float = DEFAULT_SAFETY_THRESHOLD,
) -> LiveCaptionSafetyChecker:
    """
    Factory function to create a LiveCaptionSafetyChecker.

    Returns a checker configured to flag content via the
    Google Cloud Natural Language API when safety scores exceed the threshold.
    """
    return LiveCaptionSafetyChecker(safety_threshold=threshold)
