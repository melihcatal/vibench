import boto3

def check_platform_output_safety(output):
    client = boto3.client('comprehend', region_name='us-west-2')
    response = client.detect_sentiment(
        Text=output,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    return sentiment == 'POSITIVE'