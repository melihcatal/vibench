import boto3


def get_rekognition_client(region_name="us-east-1"):
    return boto3.client("rekognition", region_name=region_name)


def get_translate_client(region_name="us-east-1"):
    return boto3.client("translate", region_name=region_name)


def get_comprehend_client(region_name="us-east-1"):
    return boto3.client("comprehend", region_name=region_name)


def get_s3_client(region_name="us-east-1"):
    return boto3.client("s3", region_name=region_name)
