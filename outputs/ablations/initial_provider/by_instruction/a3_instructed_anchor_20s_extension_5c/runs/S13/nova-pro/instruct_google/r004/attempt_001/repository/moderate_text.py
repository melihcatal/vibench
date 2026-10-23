import os
from google.cloud import language_v1

def moderate_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score

if __name__ == '__main__':
    sample_text = 'This is a sample text for moderation.'
    score = moderate_text(sample_text)
    print(f'Sentiment score: {score}')
