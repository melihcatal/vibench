from google.cloud import language_v1


def check_narration_safety(text):
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude

    safety_issues = []

    if sentiment_score < -0.5:
        safety_issues.append("Highly negative sentiment")

    if sentiment_magnitude > 2.0:
        safety_issues.append("Strong emotional content")

    try:
        classify_response = client.classify_text(request={"document": document})

        for category in classify_response.categories:
            if any(
                unsafe_term in category.name.lower()
                for unsafe_term in ["violence", "hate", "adult"]
            ):
                safety_issues.append(f"Potential unsafe category: {category.name}")
    except:
        pass

    return {
        "is_safe": len(safety_issues) == 0,
        "safety_issues": safety_issues,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
    }
