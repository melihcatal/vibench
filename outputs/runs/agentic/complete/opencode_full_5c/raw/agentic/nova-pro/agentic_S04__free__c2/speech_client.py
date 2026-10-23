import boto3


def get_transcribe_client():
    return boto3.client("transcribe")


def get_translate_client():
    return boto3.client("translate")


def get_comprehend_client():
    return boto3.client("comprehend")
