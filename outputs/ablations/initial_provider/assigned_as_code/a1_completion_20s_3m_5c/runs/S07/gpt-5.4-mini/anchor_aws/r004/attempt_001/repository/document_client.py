import boto3

from document_models import normalize_region


def textract_client(config=None):
    return boto3.client("textract", region_name=normalize_region(config))


def amazon_translate_client(config=None):
    return boto3.client("translate", region_name=normalize_region(config))


def amazon_comprehend_client(config=None):
    return boto3.client("comprehend", region_name=normalize_region(config))


def amazon_bedrock_client(config=None):
    return boto3.client("bedrock-runtime", region_name=normalize_region(config))
