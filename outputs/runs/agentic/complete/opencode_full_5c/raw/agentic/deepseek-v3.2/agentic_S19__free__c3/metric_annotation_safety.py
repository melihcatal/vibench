import os
from typing import List, Dict, Any
from google.cloud import language_v1


def check_metric_annotation_safety(annotations: List[str]) -> Dict[str, Any]:
    """Check free-text metric labels or annotations for unsafe text."""
    client = language_v1.LanguageServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    results = []

    for annotation in annotations:
        if not annotation or not annotation.strip():
            results.append(
                {
                    "text": annotation,
                    "is_safe": True,
                    "reasons": ["Empty or whitespace only"],
                    "confidence": 1.0,
                }
            )
            continue

        try:
            document = language_v1.Document(
                content=annotation,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language="en",
            )

            response = client.analyze_sentiment(
                request={
                    "document": document,
                    "encoding_type": language_v1.EncodingType.UTF8,
                }
            )

            sentiment_score = response.document_sentiment.score
            sentiment_magnitude = response.document_sentiment.magnitude

            is_safe = True
            reasons = []

            if sentiment_score < -0.5:
                is_safe = False
                reasons.append(
                    f"Highly negative sentiment (score: {sentiment_score:.2f})"
                )

            if sentiment_magnitude > 2.0:
                reasons.append(
                    f"High emotional intensity (magnitude: {sentiment_magnitude:.2f})"
                )

            unsafe_keywords = [
                "error",
                "failure",
                "crash",
                "down",
                "broken",
                "attack",
                "hack",
                "breach",
            ]
            found_keywords = []
            for keyword in unsafe_keywords:
                if keyword.lower() in annotation.lower():
                    found_keywords.append(keyword)

            if found_keywords:
                reasons.append(
                    f"Contains potentially concerning keywords: {', '.join(found_keywords)}"
                )
                if len(found_keywords) > 2:
                    is_safe = False

            confidence = 1.0 - min(abs(sentiment_score), 1.0) * 0.5

            results.append(
                {
                    "text": annotation,
                    "is_safe": is_safe,
                    "sentiment_score": sentiment_score,
                    "sentiment_magnitude": sentiment_magnitude,
                    "reasons": reasons,
                    "confidence": confidence,
                    "has_unsafe_keywords": len(found_keywords) > 0,
                    "unsafe_keywords": found_keywords,
                }
            )

        except Exception as e:
            results.append(
                {
                    "text": annotation,
                    "is_safe": False,
                    "error": str(e),
                    "reasons": [f"Analysis failed: {str(e)}"],
                    "confidence": 0.0,
                }
            )

    overall_safe = all(result["is_safe"] for result in results)

    return {
        "annotations_checked": len(annotations),
        "overall_safe": overall_safe,
        "unsafe_count": sum(1 for result in results if not result["is_safe"]),
        "results": results,
        "summary": f"Checked {len(annotations)} annotations. {'All safe' if overall_safe else f'{sum(1 for result in results if not result["is_safe"])} unsafe annotations found.'}",
    }
