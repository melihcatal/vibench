import os
from google.cloud import language_v1
from messaging_models import ProcessedMessage

client = language_v1.LanguageServiceClient()

def check_message_safety(processed_message: ProcessedMessage) -> bool:
    document = language_v1.Document(
        content=str(processed_message.payload),
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment
    
    # Check for extreme sentiment scores or toxic content
    if sentiment.score < -0.8 or sentiment.magnitude > 0.9:
        return False
    
    return True