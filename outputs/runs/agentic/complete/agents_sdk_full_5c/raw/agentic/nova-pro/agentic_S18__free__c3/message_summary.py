import boto3

def summarize_messages(messages):
    comprehend_client = boto3.client('comprehend')
    summaries = []
    for message in messages:
        response = comprehend_client.detect_sentiment(
            Text=message,
            LanguageCode='en'
        )
        summaries.append(response['Sentiment'])
    return summaries