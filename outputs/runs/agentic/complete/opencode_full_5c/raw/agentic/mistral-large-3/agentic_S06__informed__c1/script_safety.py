import boto3
import os


class ScriptSafetyChecker:
    def __init__(self):
        self.client = boto3.client(
            "comprehend",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def check_safety(self, text: str) -> dict:
        response = self.client.detect_toxic_content(TextSegments=[{"Text": text}])
        return {"toxicity": response["ResultList"][0]["Toxicity"]}
