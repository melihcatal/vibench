import boto3

class VisionClient:
    def __init__(self, region_name='us-east-1'):
        self.rekognition_client = boto3.client('rekognition', region_name=region_name)
        self.comprehend_client = boto3.client('comprehend', region_name=region_name)
        self.translate_client = boto3.client('translate', region_name=region_name)
        self.s3_client = boto3.client('s3', region_name=region_name)
