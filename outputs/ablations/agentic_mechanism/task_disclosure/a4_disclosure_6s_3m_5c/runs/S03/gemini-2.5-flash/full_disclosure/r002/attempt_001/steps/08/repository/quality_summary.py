from google.cloud import language_v1

def summarize_quality_issues(text: str) -> dict:
    """
    Summarizes translation quality issues using Google Cloud Natural Language API.

    Args:
        text: The translated text to analyze.

    Returns:
        A dictionary summarizing potential quality issues.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    summary = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "potential_issues": []
    }

    if sentiment.score < -0.25:
        summary["potential_issues"].append("Overall negative sentiment detected, which might indicate a quality issue or inappropriate tone.")
    elif sentiment.magnitude > 1.5 and abs(sentiment.score) < 0.25:
        summary["potential_issues"].append("High magnitude with neutral sentiment, potentially indicating a lack of clear emotional tone where one might be expected.")

    # In a real-world scenario, more sophisticated analysis would be done here,
    # e.g., entity analysis for incorrect entities, syntax analysis for grammatical errors,
    # or custom quality checks based on specific translation requirements.

    return summary
