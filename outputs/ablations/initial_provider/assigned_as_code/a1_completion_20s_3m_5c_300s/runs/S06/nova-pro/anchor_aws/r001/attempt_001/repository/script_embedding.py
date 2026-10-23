import boto3


def embed_script(text):
    client = boto3.client('comprehend')
    response = client.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    return response['Sentiment']