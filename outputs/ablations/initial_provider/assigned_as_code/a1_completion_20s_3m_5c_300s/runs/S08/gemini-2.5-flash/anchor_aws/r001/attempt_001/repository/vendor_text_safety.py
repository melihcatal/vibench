from google.cloud import language_v2 as language
from typing import Dict, Any
from document_client import load_config

def moderate_vendor_text(text: str) -> Dict[str, Any]:
    config = load_config()
    project_id = config.get("google_project_id") # Google Cloud NL client might need project_id

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Google Cloud Natural Language.")

    client = language.LanguageServiceClient()

    document = language.Document(
        content=text, type=language.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis as a proxy for safety/moderation. 
    # A dedicated moderation API would be ideal, but for the purpose of demonstrating a 'concrete provider' for safety,
    # sentiment analysis can indicate potentially unsafe content if sentiment is very negative.
    # For real-world safety, Google Cloud provides the Perspective API, but it's not part of the standard client.
    # Using standard Natural Language API for sentiment, which is widely available.
    response = client.analyze_sentiment(document=document, encoding_type=language.EncodingType.UTF8)
    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude

    # Basic moderation logic based on sentiment
    is_safe = True
    safety_notes = []

    if sentiment_score < -0.5 and sentiment_magnitude > 1.0:
        is_safe = False
        safety_notes.append("Text sentiment is highly negative, may require review.")
    
    # In a real scenario, more sophisticated entity analysis or custom classification might be used.
    # For this task, we focus on demonstrating the use of a concrete provider.

    return {"is_safe": is_safe, "sentiment_score": sentiment_score, "sentiment_magnitude": sentiment_magnitude, "safety_notes": safety_notes}
