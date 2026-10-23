from google.cloud import language_v1
import os

def check_log_text_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    
    document = language_v1.Document(
        content=text, 
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_sentiment(
        request={"document": document}
    )
    
    # Google Cloud Natural Language API safety classification
    safety_attributes = response.document_sentiment
    
    return {
        "safety_score": safety_attributes.score,
        "safety_magnitude": safety_attributes.magnitude,
        "is_unsafe": safety_attributes.score < -0.5
    }