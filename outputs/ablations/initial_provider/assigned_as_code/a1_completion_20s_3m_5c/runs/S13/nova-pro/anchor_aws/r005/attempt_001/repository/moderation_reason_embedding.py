import boto3


def embed_text(text):
    comprehend = boto3.client('comprehend')
    result = comprehend.detect_dominant_language(Text=text)
    language_code = result['Languages'][0]['LanguageCode']
    result = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return result['Sentiment']