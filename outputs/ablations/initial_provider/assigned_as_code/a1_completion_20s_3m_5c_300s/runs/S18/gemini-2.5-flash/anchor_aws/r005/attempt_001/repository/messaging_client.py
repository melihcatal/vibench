import boto3


def get_sns_client(region_name):
    return boto3.client("sns", region_name=region_name)


def get_sqs_client(region_name):
    return boto3.client("sqs", region_name=region_name)

def get_comprehend_client(region_name):
    return boto3.client("comprehend", region_name=region_name)

def get_translate_client(region_name):
    return boto3.client("translate", region_name=region_name)

def get_dynamodb_client(region_name):
    return boto3.client("dynamodb", region_name=region_name)
