import boto3

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

comprehend = boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def safety_threshold(text, threshold=0.5):
    response = comprehend.detect_toxic_content(Text=text)
    toxicity_score = response['Entities'][0]['Score'] if response['Entities'] else 0
    return toxicity_score < threshold