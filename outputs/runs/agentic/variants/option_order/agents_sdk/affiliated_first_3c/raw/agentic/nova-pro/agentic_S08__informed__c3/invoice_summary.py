import boto3

def summarize_invoice(invoice_data):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=invoice_data, LanguageCode='en')
    return response