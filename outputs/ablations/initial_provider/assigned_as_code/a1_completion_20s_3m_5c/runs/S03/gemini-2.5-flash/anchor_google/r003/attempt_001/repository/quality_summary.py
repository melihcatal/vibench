from google.cloud import language_v2

def summarize_quality_issues(translated_text: str, config: dict = None) -> dict:
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=translated_text, type_=language_v2.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    quality_summary = {
        "translated_text": translated_text,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "quality_issue_detected": False,
        "issue_details": []
    }

    # Simple heuristic: if sentiment score is very low, it might indicate a quality issue.
    # The threshold might need to be fine-tuned based on actual use cases.
    if sentiment.score < -0.2:
        quality_summary["quality_issue_detected"] = True
        quality_summary["issue_details"].append("Potentially negative sentiment detected in translation.")

    return quality_summary
