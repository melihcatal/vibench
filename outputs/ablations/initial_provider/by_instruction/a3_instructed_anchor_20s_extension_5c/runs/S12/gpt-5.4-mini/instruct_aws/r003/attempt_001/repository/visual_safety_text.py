import boto3


def main(text: str):
    return {"provider": "aws.comprehend", "text": text, "client": boto3.client("comprehend")}
