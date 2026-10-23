import boto3
from document_client import get_comprehend_client

def ocr_embedding(text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode=language_code)
    return response['Sentiment']