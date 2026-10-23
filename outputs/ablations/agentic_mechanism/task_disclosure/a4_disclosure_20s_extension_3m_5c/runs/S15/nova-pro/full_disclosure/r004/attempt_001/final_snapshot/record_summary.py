import boto3

def summarize_document_records(document_records):
    comprehend = boto3.client('comprehend')
    summaries = []
    for record in document_records:
        if 'text' in record:
            summary = comprehend.detect_sentiment(Text=record['text'], LanguageCode='en')
            summaries.append(summary)
    return summaries