from google.cloud.language_v1 import enums

def normalize_sentiment(sentiment):
    return {
        'score': sentiment.score,
        'magnitude': sentiment.magnitude,
        'language': enums.Document.Type.Name(sentiment.language)
    }