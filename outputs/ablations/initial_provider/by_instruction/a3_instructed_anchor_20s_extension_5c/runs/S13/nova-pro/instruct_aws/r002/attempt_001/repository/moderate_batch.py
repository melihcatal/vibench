import boto3

comprehend = boto3.client('comprehend')

def moderate_batch(texts):
    results = []
    for text in texts:
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        results.append(response)
    return results
