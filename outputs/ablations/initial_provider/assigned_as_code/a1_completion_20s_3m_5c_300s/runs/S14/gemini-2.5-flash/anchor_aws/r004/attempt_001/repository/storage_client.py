import boto3
from storage_models import StorageConfig

def get_s3_client(config: StorageConfig):
    return boto3.client("s3", region_name=config.region)

def get_textract_client(config: StorageConfig):
    return boto3.client("textract", region_name=config.region)

def get_translate_client(config: StorageConfig):
    return boto3.client("translate", region_name=config.region)

def get_comprehend_client(config: StorageConfig):
    return boto3.client("comprehend", region_name=config.region)

def get_bedrock_runtime_client(config: StorageConfig):
    return boto3.client("bedrock-runtime", region_name=config.region)
