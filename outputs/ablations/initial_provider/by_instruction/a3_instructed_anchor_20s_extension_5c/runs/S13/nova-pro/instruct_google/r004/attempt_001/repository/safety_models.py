from google.cloud import language_v1

def normalize_sentiment_response(response):
    return response.document_sentiment.score
