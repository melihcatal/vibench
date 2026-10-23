import boto3

def vendor_text_safety(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_toxic_content(Text=text)
    return response