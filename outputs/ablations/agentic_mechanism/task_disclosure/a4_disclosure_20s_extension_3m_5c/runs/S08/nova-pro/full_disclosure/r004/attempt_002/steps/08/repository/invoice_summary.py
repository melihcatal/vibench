import boto3

def summarize_invoice_fields(invoice_fields):
    comprehend = boto3.client('comprehend')
    summary = comprehend.summarize_text(
        Text=str(invoice_fields),
        LanguageCode='en'
    )
    return summary['Summary']