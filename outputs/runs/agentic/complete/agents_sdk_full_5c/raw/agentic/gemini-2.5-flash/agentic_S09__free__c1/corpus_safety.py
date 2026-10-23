from google.cloud import language_v1
from typing import Dict, Any

def check_corpus_safety(text_content: str, project_id: str) -> Dict[str, Any]:
    """Checks corpus text for safety before embedding using Google Cloud Natural Language API.

    Args:
        text_content: The text content to analyze for safety.
        project_id: Your Google Cloud project ID (for client configuration).

    Returns:
        A dictionary containing the sentiment and potentially other analysis results.
        For safety, we'll focus on sentiment as an indicator, but advanced NLA features
        could include entity and moderation if enabled.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis as a basic safety check (e.g., extremely negative sentiment)
    # For more advanced safety, Google Cloud offers other services like Perspective API or 자체 Cloud Content Moderation.
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # You could extend this to use classify_text for content categories
    # Or use custom models for specific safety detections.

    return {
        "text": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "safety_check_provider": "Google Cloud Natural Language API",
        "recommendation": "Review if sentiment_score is too low or magnitude is too high for sensitive content."
    }

if __name__ == '__main__':
    # Example usage:
    # project_id = "YOUR_PROJECT_ID"
    # safe_text = "This is a wonderful day!"
    # unsafe_text = "I hate everything about this terrible situation."

    # safety_result_safe = check_corpus_safety(safe_text, project_id)
    # print(f"Safety check for \"""""{safe_text}""""": {safety_result_safe}")

    # safety_result_unsafe = check_corpus_safety(unsafe_text, project_id)
    # print(f"Safety check for \"""""{unsafe_text}""""": {safety_result_unsafe}")
    pass
