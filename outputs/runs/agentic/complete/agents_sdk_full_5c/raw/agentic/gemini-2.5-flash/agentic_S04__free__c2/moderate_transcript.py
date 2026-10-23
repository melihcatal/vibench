from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPIError

def moderate_transcript_text(text_content: str) -> dict:
    """Moderates transcript text using Google Cloud Natural Language API (sentiment analysis as a proxy).

    Args:
        text_content: The full transcript text to moderate.

    Returns:
        A dictionary containing sentiment analysis results (score and magnitude).
        A score of 0 indicates neutral, >0 positive, <0 negative. Magnitude indicates strength.
    """
    # Google Cloud Natural Language API client
    # Service identifiable by language_v1.LanguageServiceClient()
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    try:
        # Google Cloud Natural Language API Call for sentiment analysis
        # API identifiable by language_v1.LanguageServiceClient().analyze_sentiment
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
        moderation_result = {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        }
        print(f"Sentiment Score: {sentiment.score}, Magnitude: {sentiment.magnitude}")
        
        # Basic moderation logic based on sentiment
        if sentiment.score < -0.2 and sentiment.magnitude > 0.5:
            print("Warning: Potentially negative or strong sentiment detected.")
        elif sentiment.score > 0.2 and sentiment.magnitude > 0.5:
            print("Info: Potentially positive or strong sentiment detected.")
        else:
            print("Info: Neutral or mild sentiment detected.")

        return moderation_result
    except GoogleAPIError as e:
        print(f"Error moderating transcript text: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    transcript_text_positive = "The meeting was incredibly productive and everyone was very happy."
    transcript_text_negative = "I am extremely disappointed with the outcome and the poor communication."
    transcript_text_neutral = "The meeting covered the agenda items."

    print("\n--- Moderating Positive Text ---")
    try:
        moderate_transcript_text(transcript_text_positive)
    except Exception as e:
        print(f"Failed to moderate: {e}")

    print("\n--- Moderating Negative Text ---")
    try:
        moderate_transcript_text(transcript_text_negative)
    except Exception as e:
        print(f"Failed to moderate: {e}")

    print("\n--- Moderating Neutral Text ---")
    try:
        moderate_transcript_text(transcript_text_neutral)
    except Exception as e:
        print(f"Failed to moderate: {e}")
