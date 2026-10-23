import os
from google.cloud import language_v1

def visual_safety_text(payload, config=None):
    config = config or {}

    client = language_v1.LanguageServiceClient()

    text_content = payload.get('text')
    if not text_content:
        return {'safety_analysis': None}

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze for sentiment, entities, and categories which can help infer safety
    # For explicit safety/moderation, a dedicated content moderation API is usually better.
    # However, for this task, we will use Natural Language for text analysis.
    response = client.analyze_sentiment(document=document)
    sentiment = {
        'score': response.document_sentiment.score,
        'magnitude': response.document_sentiment.magnitude
    }

    # You can also analyze entities and categories for more detailed insights
    # For simplicity, we'll just return sentiment for now.

    return {
        'safety_analysis': {
            'sentiment': sentiment,
            # 'categories': categories_result,
            # 'entities': entities_result
        }
    }
