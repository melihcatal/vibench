import boto3

def embed_script(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_dominant_language(
        Text=text
    )
    language = response['Languages'][0]['LanguageCode']
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode=language
    )
    sentiment = response['Sentiment']
    return sentiment