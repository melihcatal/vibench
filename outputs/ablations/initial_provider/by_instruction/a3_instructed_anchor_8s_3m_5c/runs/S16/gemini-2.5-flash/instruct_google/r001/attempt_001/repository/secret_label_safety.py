from google.cloud import language_v2
from google.cloud.language_v2 import types
from security_models import SecretMetadata

def check_secret_label_safety(text: str) -> dict:
    client = language_v2.LanguageServiceClient()
    document = types.Document(content=text, type_=types.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    # The Natural Language API doesn't directly provide a 'safety' score like some other APIs.
    # For this task, we can use sentiment as a proxy or check for specific entities/categories
    # if the goal is to identify PII or sensitive info.
    # For simplicity, this example will just return the sentiment score.
    # In a real-world scenario, you might integrate with a dedicated content moderation API or
    # build custom logic based on entity extraction and custom classification.
    return {
        "text": text,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude
    }
