import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def moderation_summary(decisions):
    summary = {}
    for decision in decisions:
        if decision["ToxicContentDetected"]:
            summary["unsafe"] = summary.get("unsafe", 0) + 1
        else:
            summary["safe"] = summary.get("safe", 0) + 1
    return summary
