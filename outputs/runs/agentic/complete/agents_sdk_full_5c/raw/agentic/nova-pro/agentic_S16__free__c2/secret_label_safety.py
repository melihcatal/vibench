import boto3
import comprehend

def check_secret_labels(secret_id):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(SecretId=secret_id)
    labels = describe_secret_response['Name']
    comprehend_client = comprehend.Client()
    response = comprehend_client.detect_sentiment(
        Text=labels,
        LanguageCode='en'
    )
    return response['Sentiment']