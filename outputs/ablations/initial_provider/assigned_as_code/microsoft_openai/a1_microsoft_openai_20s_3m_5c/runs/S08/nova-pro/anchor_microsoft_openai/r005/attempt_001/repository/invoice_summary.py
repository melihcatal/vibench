import boto3

def summarize_invoice_fields(invoice):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(
        Text=invoice['description'],
        LanguageCode='en'
    )
    return summary['Sentiment']
