from google.cloud import language_v1
import os

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud Natural Language API for sentiment analysis.
    A negative sentiment might flag content for review.
    """
    client = language_v1.LanguageServiceClient()
    
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    try:
        # Perform sentiment analysis
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
        # You can define moderation rules based on score and magnitude
        # For example, a score < -0.2 might indicate potentially negative content
        # and a high magnitude would indicate strong emotion.
        
        is_flagged = False
        flag_reason = ""
        if sentiment.score < -0.2 and sentiment.magnitude > 0.5:
            is_flagged = True
            flag_reason = "Potentially negative sentiment detected."
        elif sentiment.score < 0 and sentiment.magnitude > 1.0:
            is_flagged = True
            flag_reason = "Strong negative emotion detected."
            
        return {
            "text": text,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "is_flagged_for_review": is_flagged,
            "flag_reason": flag_reason,
            "message": "Profile text moderation completed."
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # profile_text_good = "I am excited to join this community!"
    # profile_text_bad = "I hate everything about this platform."
    # result_good = moderate_profile_text(profile_text_good)
    # print(result_good)
    # result_bad = moderate_profile_text(profile_text_bad)
    # print(result_bad)
    pass
