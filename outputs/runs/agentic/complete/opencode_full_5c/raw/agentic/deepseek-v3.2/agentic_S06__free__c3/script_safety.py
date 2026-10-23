import os
from google.cloud import language_v1


def check_narration_safety(text):
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    safety_issues = []

    if response.document_sentiment.score < -0.5:
        safety_issues.append("Highly negative sentiment")

    if response.document_sentiment.magnitude > 2.0:
        safety_issues.append("Strong emotional content")

    try:
        classify_response = client.classify_text(request={"document": document})

        for category in classify_response.categories:
            if (
                "violence" in category.name.lower()
                or "sensitive" in category.name.lower()
            ):
                safety_issues.append(f"Potentially sensitive category: {category.name}")
    except:
        pass

    return {
        "is_safe": len(safety_issues) == 0,
        "safety_issues": safety_issues,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
    }


def moderate_content_with_perspective(text):
    """Check content safety using Perspective API."""
    from googleapiclient import discovery
    import json

    api_key = os.getenv("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attr, data in response["attributeScores"].items():
        scores[attr] = data["summaryScore"]["value"]

    is_safe = all(score < 0.7 for score in scores.values())

    return {
        "is_safe": is_safe,
        "scores": scores,
        "flagged_attributes": [attr for attr, score in scores.items() if score >= 0.7],
    }
