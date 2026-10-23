import boto3
from typing import Dict, Any

def get_s3_client(config: Dict[str, Any]) -> boto3.client:
    return boto3.client("s3", region_name=config.get("region"))

def get_textract_client(config: Dict[str, Any]) -> boto3.client:
    return boto3.client("textract", region_name=config.get("region"))

def get_translate_client(config: Dict[str, Any]) -> boto3.client:
    return boto3.client("translate", region_name=config.get("region"))

def get_comprehend_client(config: Dict[str, Any]) -> boto3.client:
    return boto3.client("comprehend", region_name=config.get("region"))

def get_openai_client(api_key: str):
    from openai import OpenAI
    return OpenAI(api_key=api_key)
