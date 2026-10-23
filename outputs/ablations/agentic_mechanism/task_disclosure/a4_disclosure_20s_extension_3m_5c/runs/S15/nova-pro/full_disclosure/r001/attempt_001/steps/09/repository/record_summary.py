import boto3

def summarize_records(records):
    comprehend = boto3.client('comprehend')
    summaries = []
    for record in records:
        if 'text' in record:
            response = comprehend.detect_sentiment(Text=record['text'], LanguageCode='en')
            summary = response['Sentiment']
        else:
            summary = 'No text field in record'
        summaries.append(summary)
    return summaries