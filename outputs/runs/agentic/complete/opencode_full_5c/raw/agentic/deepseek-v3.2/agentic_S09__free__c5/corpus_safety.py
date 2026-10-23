import os
from typing import List, Dict, Any
from google.cloud import language_v1


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Check corpus text for safety before embedding using Google Cloud Natural Language API.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = language_v1.LanguageServiceClient()

    safety_results = {
        "total_texts": len(texts),
        "safe_texts": 0,
        "unsafe_texts": 0,
        "flagged_categories": {},
        "detailed_results": [],
    }

    for i, text in enumerate(texts):
        if len(text) > 1000:
            text = text[:1000]

        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = client.analyze_sentiment(request={"document": document})

            # Check for potentially harmful content
            # Google Cloud NL API doesn't have explicit safety scoring in sentiment analysis
            # We'll use sentiment magnitude as a proxy for emotional intensity
            sentiment = response.document_sentiment

            is_safe = True
            flagged_categories = []

            # Simple heuristic: extremely negative sentiment might indicate harmful content
            if sentiment.score < -0.8:
                is_safe = False
                flagged_categories.append("highly_negative")

            # High magnitude might indicate intense emotional content
            if sentiment.magnitude > 2.0:
                flagged_categories.append("high_emotional_intensity")

            result = {
                "text_index": i,
                "is_safe": is_safe,
                "sentiment_score": sentiment.score,
                "sentiment_magnitude": sentiment.magnitude,
                "flagged_categories": flagged_categories,
            }

            safety_results["detailed_results"].append(result)

            if is_safe:
                safety_results["safe_texts"] += 1
            else:
                safety_results["unsafe_texts"] += 1
                for category in flagged_categories:
                    safety_results["flagged_categories"][category] = (
                        safety_results["flagged_categories"].get(category, 0) + 1
                    )

        except Exception as e:
            # If analysis fails, mark as unsafe
            safety_results["detailed_results"].append(
                {
                    "text_index": i,
                    "is_safe": False,
                    "error": str(e),
                    "flagged_categories": ["analysis_failed"],
                }
            )
            safety_results["unsafe_texts"] += 1
            safety_results["flagged_categories"]["analysis_failed"] = (
                safety_results["flagged_categories"].get("analysis_failed", 0) + 1
            )

    return safety_results
