import boto3


def embed_text(text):
    client = boto3.client('comprehend')
    response = client.detect_dominant_language(Text=text)
    lang_code = response['Languages'][0]['LanguageCode']
    embeddings = client.detect_sentiment(Text=text, LanguageCode=lang_code)['SentimentScore']
    return embeddings