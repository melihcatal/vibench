import boto3

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

comprehend = boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def moderate_batch(texts):
    responses = []
    for text in texts:
        response = comprehend.detect_toxic_content(Text=text)
        responses.append(response)
    return responses