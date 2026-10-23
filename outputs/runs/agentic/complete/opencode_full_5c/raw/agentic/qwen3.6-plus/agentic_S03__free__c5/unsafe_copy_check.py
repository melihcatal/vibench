from google.cloud import language_v1
from google.cloud.language_v1 import types as language_types


GOOGLE_PERSPECTIVE_API_ENDPOINT = "commentanalyzer.googleapis.com"
GOOGLE_NL_SAFE_SEARCH_MODEL = "language-v1-safe-search"


UNSAFE_CATEGORIES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "IDENTITY_ATTACK",
]


def check_unsafe_copy(
    translated_texts: list, threshold: float = 0.5, target_language: str = "es"
) -> dict:
    client = language_v1.LanguageServiceClient()

    flagged_segments = []
    total_checked = len(translated_texts)

    for i, text in enumerate(translated_texts):
        if not text or not text.strip():
            continue

        document = language_types.Document(
            content=text,
            type_=language_types.Document.Type.PLAIN_TEXT,
            language=target_language,
        )

        try:
            sentiment_response = client.analyze_sentiment(
                request={"document": document}
            )
            sentiment = sentiment_response.document_sentiment

            if sentiment.score < -0.5:
                flagged_segments.append(
                    {
                        "index": i,
                        "text": text,
                        "flag_type": "negative_sentiment",
                        "confidence": abs(sentiment.score),
                        "severity": "warning",
                        "details": f"Sentiment score: {sentiment.score:.2f}",
                    }
                )

            entities_response = client.analyze_entities(request={"document": document})
            for entity in entities_response.entities:
                if (
                    entity.type_ == language_types.Entity.Type.PERSON
                    and entity.salience > 0.7
                ):
                    flagged_segments.append(
                        {
                            "index": i,
                            "text": text,
                            "flag_type": "personal_reference",
                            "confidence": entity.salience,
                            "severity": "info",
                            "details": f"Personal entity '{entity.name}' detected (salience: {entity.salience:.2f})",
                        }
                    )

        except Exception as e:
            flagged_segments.append(
                {
                    "index": i,
                    "text": text,
                    "flag_type": "analysis_error",
                    "confidence": 0.0,
                    "severity": "error",
                    "details": str(e),
                }
            )

    is_safe = len(flagged_segments) == 0

    return {
        "is_safe": is_safe,
        "total_checked": total_checked,
        "flagged_count": len(flagged_segments),
        "flagged_segments": flagged_segments,
        "threshold": threshold,
        "provider": "google-cloud-natural-language",
        "model": GOOGLE_NL_SAFE_SEARCH_MODEL,
    }
