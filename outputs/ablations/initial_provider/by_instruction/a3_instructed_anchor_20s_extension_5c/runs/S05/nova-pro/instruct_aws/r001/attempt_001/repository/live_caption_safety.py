import boto3

def check_safety(captions):
    client = boto3.client('comprehend')
    # Safety check logic here
    pass