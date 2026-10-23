from safety_client import get_language_client
from safety_models import normalize_sentiment

def moderation_summary(texts):
    client = get_language_client()
    summaries = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment
        summaries.append(normalize_sentiment(sentiment))
    return summaries