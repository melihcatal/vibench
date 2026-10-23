import boto3

def get_rekognition_client(region_name):
    return boto3.client("rekognition", region_name=region_name)
