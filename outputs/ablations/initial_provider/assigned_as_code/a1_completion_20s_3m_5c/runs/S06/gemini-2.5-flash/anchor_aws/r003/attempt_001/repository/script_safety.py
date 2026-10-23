from google.cloud import language_v1
import os

def check_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # Using analyze_sentiment as a basic safety check proxy. For more advanced safety, 
    # other specialized APIs or custom models would be needed.
    response = client.analyze_sentiment(document=document)
    
    # This is a simplified safety check. A real safety check would involve more robust analysis.
    # For demonstration, we'll just return sentiment score.
    return {
        "score": response.document_sentiment.score,
        "magnitude": response.document_sentiment.magnitude,
        "is_safe": response.document_sentiment.score >= -0.2 # Arbitrary threshold for "safe"
    }
