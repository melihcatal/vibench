import boto3

def check_log_text_safety(log_text):
    client = boto3.client('comprehend', region_name='us-west-2')
    response = client.detect_toxic_content(
        TextSegments=[{
            'Text': log_text
        }]
    )
    return response['ToxicContent']