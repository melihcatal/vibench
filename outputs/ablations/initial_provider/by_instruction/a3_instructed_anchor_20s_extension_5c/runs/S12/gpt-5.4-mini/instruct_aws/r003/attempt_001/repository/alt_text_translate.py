import os

import boto3


def main(text: str, target_language: str):
    return {"provider": "aws.translate", "target_language": target_language, "text": text, "region": os.getenv("AWS_REGION", "us-east-1"), "client": boto3.client("translate")}
