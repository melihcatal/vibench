import boto3
from typing import Dict, Any


def get_kms_client(region_name: str):
    return boto3.client("kms", region_name=region_name)

def get_macie_client(region_name: str):
    return boto3.client("macie2", region_name=region_name)

def get_translate_client(region_name: str):
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(region_name: str):
    return boto3.client("comprehend", region_name=region_name)

def get_sagemaker_runtime_client(region_name: str):
    return boto3.client("sagemaker-runtime", region_name=region_name)

def get_cloudtrail_client(region_name: str):
    return boto3.client("cloudtrail", region_name=region_name)

def get_cloudwatch_logs_client(region_name: str):
    return boto3.client("logs", region_name=region_name)
