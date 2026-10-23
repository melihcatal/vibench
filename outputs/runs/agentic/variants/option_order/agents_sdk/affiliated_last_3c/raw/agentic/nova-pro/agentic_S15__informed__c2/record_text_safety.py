import boto3

comprehend = boto3.client('comprehend', region_name='us-west-2', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')

def check_text_safety(text):
    response = comprehend.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['Results'][0]['Toxicity']