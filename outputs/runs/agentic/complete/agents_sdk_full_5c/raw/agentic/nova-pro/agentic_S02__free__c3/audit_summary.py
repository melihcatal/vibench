import boto3

def audit_summary(audit_records):
    comprehend = boto3.client('comprehend')
    summaries = []
    for record in audit_records:
        response = comprehend.detect_sentiment(Text=record, LanguageCode='en')
        summaries.append(response['Sentiment'])
    return summaries