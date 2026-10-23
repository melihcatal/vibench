import os
from google.cloud import language_v1


def message_safety(payload_text):
    """Check message payload text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    if not payload_text or not isinstance(payload_text, str):
        return {"safe": True, "reason": "No text to analyze"}

    document = language_v1.Document(
        content=payload_text[:1000],
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    try:
        response = client.analyze_sentiment(request={"document": document})

        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude

        is_safe = True
        safety_issues = []

        if sentiment_score < -0.5:
            is_safe = False
            safety_issues.append("Highly negative sentiment")

        if sentiment_magnitude > 2.0:
            safety_issues.append("High emotional intensity")

        categories_response = client.classify_text(request={"document": document})

        unsafe_categories = ["/Law & Government", "/Sensitive Subjects", "/Adult"]
        for category in categories_response.categories:
            for unsafe in unsafe_categories:
                if unsafe in category.name:
                    is_safe = False
                    safety_issues.append(f"Unsafe category: {category.name}")
                    break

        return {
            "safe": is_safe,
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "safety_issues": safety_issues if safety_issues else ["No issues detected"],
            "text_sample": payload_text[:200],
        }

    except Exception as e:
        return {"safe": False, "error": str(e), "safety_issues": ["Analysis failed"]}
