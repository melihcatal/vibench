import os
from google.cloud import language_v1

def apply_safety_threshold(text, threshold=-0.5):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score >= threshold

if __name__ == '__main__':
    sample_text = 'This is a text to apply safety threshold.'
    is_safe = apply_safety_threshold(sample_text)
    print(f'Is safe: {is_safe}')
