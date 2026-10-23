import os
from google.cloud import language_v1

def redact_unsafe(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment_score = response.document_sentiment.score
    if sentiment_score < -0.5:
        return '[REDACTED]'
    return text

if __name__ == '__main__':
    text = 'Your text here'
    redacted_text = redact_unsafe(text)
    print(f'Redacted Text: {redacted_text}')
