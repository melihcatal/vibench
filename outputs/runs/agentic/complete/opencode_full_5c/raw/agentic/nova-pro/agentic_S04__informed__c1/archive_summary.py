import os
import boto3


def archive_summary(transcript):
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    summary = comprehend.summarize(Text=transcript)
    return summary
