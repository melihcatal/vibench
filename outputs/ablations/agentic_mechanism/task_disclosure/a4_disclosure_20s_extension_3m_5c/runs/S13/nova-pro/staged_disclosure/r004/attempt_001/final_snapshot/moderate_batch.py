import boto3

def moderate_batch(messages):
    comprehend = boto3.client('comprehend')
    results = []
    for message in messages:
        response = comprehend.detect_toxic_content(
            Text=message,
            LanguageCode='en'
        )
        results.append(response['Labels'])
    return results
