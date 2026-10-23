import boto3
import os

titan_embeddings_client = boto3.client("bedrock-runtime", region_name="us-west-2")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
