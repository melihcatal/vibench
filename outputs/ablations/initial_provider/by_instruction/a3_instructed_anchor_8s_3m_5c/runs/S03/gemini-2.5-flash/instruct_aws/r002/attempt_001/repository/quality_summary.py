import boto3

def quality_summary(translated_text: str, target_language: str) -> dict:
    """
    Summarize translation quality issues using AWS Comprehend for sentiment analysis.
    This is a heuristic approach to identify potential quality concerns.
    """
    comprehend = boto3.client("comprehend")
    
    sentiment_response = comprehend.detect_sentiment(
        Text=translated_text,
        LanguageCode=target_language
    )
    
    key_phrases_response = comprehend.detect_key_phrases(
        Text=translated_text,
        LanguageCode=target_language
    )

    return {
        "sentiment": sentiment_response["Sentiment"] + " (Score: " + str(sentiment_response["SentimentScore"][sentiment_response["Sentiment"].capitalize()]) + ")",
        "key_phrases": [phrase["Text"] for phrase in key_phrases_response["KeyPhrases"]]
    }
