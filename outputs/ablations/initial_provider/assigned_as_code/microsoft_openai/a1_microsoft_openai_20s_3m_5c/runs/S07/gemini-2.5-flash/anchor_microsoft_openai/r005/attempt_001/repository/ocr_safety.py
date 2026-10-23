
import os
from google.cloud import language_v1 as language
from document_client import get_language_client
from document_models import DocumentSafetyResult

def ocr_safety(payload, config=None):
    config = config or {}
    client = get_language_client()

    document = language.Document(
        content=payload['text'],
        type_=language.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis to get a general idea, or more specifically moderation
    # For content safety, typically you'd use a dedicated moderation API or a custom model.
    # For this example, we'll use the analyze_sentiment and entity analysis for illustrative purposes
    # A more robust solution would involve a dedicated content moderation service.

    # For a basic safety check, we can analyze sentiment or entities that might indicate unsafe content
    # However, for true safety, services like Perspective API or custom models are better.
    # Let's simulate a basic check for general sentiment for this exercise.
    
    # A more appropriate tool for safety would be something like Perspective API.
    # For Google Cloud, a combination of Natural Language API (for entity/sentiment) 
    # and potentially a custom AI Platform model or a future dedicated safety API.
    # As per prompt, I need to use one concrete third-party managed service. Natural Language AI is a managed service.

    response = client.analyze_sentiment(document=document)
    
    is_safe = True
    reasons = []

    # A very basic check: if the sentiment score is very negative, it might be unsafe.
    # This is a simplification; real safety checks are more complex.
    if response.document_sentiment.score < -0.5:
        is_safe = False
        reasons.append(f"Negative sentiment detected (score: {response.document_sentiment.score})")

    # You could also analyze entities for problematic keywords
    # For a real scenario, integrate with a dedicated content moderation service.

    return DocumentSafetyResult(is_safe=is_safe, reasons=reasons)
