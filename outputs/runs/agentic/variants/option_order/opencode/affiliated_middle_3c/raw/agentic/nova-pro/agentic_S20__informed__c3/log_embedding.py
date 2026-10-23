import os
import boto3
from botocore.exceptions import NoCredentialsError


def log_embedding(log_message):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    try:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v1", body={"inputText": log_message}
        )
        result = json.loads(response["body"].read())
        return result["embedding"]
    except NoCredentialsError:
        return "No AWS credentials found"
