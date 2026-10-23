import boto3

comprehend_client = boto3.client('comprehend')

def summarize_invoice(extracted_fields):
    # Summarization logic here
    return summary