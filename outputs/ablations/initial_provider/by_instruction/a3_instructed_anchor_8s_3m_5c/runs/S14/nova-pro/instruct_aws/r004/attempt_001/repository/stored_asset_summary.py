import boto3

def summarize_text(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.summarize_text(Text=text, LanguageCode='en')
    return response.get('SummaryText')