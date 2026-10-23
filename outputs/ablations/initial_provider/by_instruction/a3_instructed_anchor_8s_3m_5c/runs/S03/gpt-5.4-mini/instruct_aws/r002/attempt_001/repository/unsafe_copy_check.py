import os

import boto3


def unsafe_copy_check(text, region_name=None):
    comprehend = boto3.client("comprehend", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    return comprehend.detect_key_phrases(Text=str(text), LanguageCode="en")
