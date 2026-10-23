import boto3


def get_transcribe_client(config):
    return boto3.client("transcribe", region_name=config.get("region"))


def get_translate_client(config):
    return boto3.client("translate", region_name=config.get("region"))


def get_comprehend_client(config):
    return boto3.client("comprehend", region_name=config.get("region"))


def get_textract_client(config):
    return boto3.client("textract", region_name=config.get("region"))