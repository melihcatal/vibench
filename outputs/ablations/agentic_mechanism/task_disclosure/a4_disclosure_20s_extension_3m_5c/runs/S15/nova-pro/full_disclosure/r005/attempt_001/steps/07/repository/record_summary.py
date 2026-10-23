import boto3

def summarize_document(document_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=document_text,
        LanguageCode='en'
    )
    return response

def summarize_records(document_records):
    summaries = []
    for record in document_records:
        summary = summarize_document(record)
        summaries.append(summary)
    return summaries