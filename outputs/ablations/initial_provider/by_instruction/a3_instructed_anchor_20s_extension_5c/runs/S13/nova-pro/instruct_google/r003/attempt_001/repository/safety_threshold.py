import os
from google.cloud import language_v1

def safety_threshold(text, threshold=-0.5):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment_score = response.document_sentiment.score
    return sentiment_score >= threshold

if __name__ == '__main__':
    text = 'Your text here'
    is_safe = safety_threshold(text)
    print(f'Is Safe: {is_safe}')
