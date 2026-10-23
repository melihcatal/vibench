import boto3

def get_translate_client(region_name=None):
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(region_name=None):
    return boto3.client("comprehend", region_name=region_name)

def get_polly_client(region_name=None):
    return boto3.client("polly", region_name=region_name)

def get_sagemaker_runtime_client(region_name=None):
    return boto3.client("sagemaker-runtime", region_name=region_name)