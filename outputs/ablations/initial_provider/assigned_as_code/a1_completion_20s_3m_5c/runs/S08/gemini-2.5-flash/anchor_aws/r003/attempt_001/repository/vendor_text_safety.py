import os
from google.cloud import language_v1 # Provider-specific import
from document_models import NormalizedExpense

# Initialize Google Cloud Natural Language client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in an environment with appropriate service account permissions.
client = language_v1.LanguageServiceClient()

def moderate_vendor_notes(expense: NormalizedExpense) -> str:
    if not expense.notes:
        expense.safety_moderation_status = "N/A - No notes"
        return "N/A - No notes to moderate."

    document = language_v1.Document(content=expense.notes, type_=language_v1.Document.Type.PLAIN_TEXT)

    try:
        # Perform sentiment analysis to get a general idea of the text
        sentiment_response = client.analyze_sentiment(document=document)
        sentiment_score = sentiment_response.document_sentiment.score
        
        # You can also use entity analysis or content classification for more specific moderation.
        # For simplicity, we'll use sentiment as a basic moderation signal.
        if sentiment_score < -0.2: # Example threshold for negative sentiment
            expense.safety_moderation_status = "Flagged - Negative Sentiment"
            return f"Flagged: Potentially negative sentiment detected (Score: {sentiment_score})."
        elif sentiment_score > 0.2:
            expense.safety_moderation_status = "Clean - Positive Sentiment"
            return f"Clean: Positive sentiment detected (Score: {sentiment_score})."
        else:
            expense.safety_moderation_status = "Clean - Neutral Sentiment"
            return f"Clean: Neutral sentiment detected (Score: {sentiment_score})."

    except Exception as e:
        print(f"Error moderating vendor notes with Google Cloud Natural Language API: {e}")
        expense.safety_moderation_status = "Error during moderation"
        return "Error during moderation."
