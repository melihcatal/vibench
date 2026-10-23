import json

from messaging_client import get_comprehend_client

def summarize_message_content(text_content: str, language_code: str = "en", region_name: str = None):
    comprehend_client = get_comprehend_client(region_name)

    # Using detect_sentiment as a form of summarization for message context
    # More advanced summarization would require more complex NLP or another AWS service
    response = comprehend_client.detect_sentiment(
        Text=text_content,
        LanguageCode=language_code
    )

    sentiment = response["Sentiment"]
    sentiment_scores = response["SentimentScore"]

    return {
        "sentiment": sentiment,
        "sentiment_scores": sentiment_scores,
        "summary_type": "sentiment_analysis"
    }
