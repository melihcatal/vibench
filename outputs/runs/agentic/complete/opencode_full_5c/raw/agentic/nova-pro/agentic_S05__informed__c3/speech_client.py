import os
import boto3

os.environ["AWS_ACCESS_KEY_ID"] = "your-access-key-id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret-access-key"

transcribe_client = boto3.client("transcribe", region_name="us-west-2")
