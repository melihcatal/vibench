import boto3


def script_embedding(text):
    client = boto3.client('comprehend')
    response = client.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    embeddings = client.detect_sentiment(Text=text, LanguageCode=language_code)['SentimentScore']
    return embeddings