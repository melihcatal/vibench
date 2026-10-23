import boto3

def audit_summary(audit_events):
    comprehend = boto3.client('comprehend')
    summaries = []
    for event in audit_events:
        response = comprehend.detect_sentiment(Text=event, LanguageCode='en')
        summaries.append(response['Sentiment'])
    return summaries