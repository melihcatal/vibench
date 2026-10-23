import boto3

def invoice_summary(invoice_fields):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(
        Text=invoice_fields.get('notes', ''),
        LanguageCode='en'
    )
    return summary