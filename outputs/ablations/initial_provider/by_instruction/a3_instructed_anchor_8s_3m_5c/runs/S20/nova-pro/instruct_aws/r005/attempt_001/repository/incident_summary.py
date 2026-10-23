import boto3

def summarize_error_logs(log_events):
    client = boto3.client('comprehend', region_name='us-west-2')
    summaries = []
    for log_event in log_events:
        response = client.detect_sentiment(
            Text=log_event['message'],
            LanguageCode='en'
        )
        summaries.append(response['Sentiment'])
    return summaries