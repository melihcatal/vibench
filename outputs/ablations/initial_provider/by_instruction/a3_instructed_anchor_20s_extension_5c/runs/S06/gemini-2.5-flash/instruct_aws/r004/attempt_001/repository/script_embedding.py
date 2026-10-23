import boto3
import os
import json

def script_embedding(text: str) -> list:
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    model_id = "amazon.titan-embed-text-v1"
    body = json.dumps({"inputText": text})
    response = bedrock_runtime_client.invoke_model(
        body=body, modelId=model_id, accept="application/json", contentType="application/json"
    )
    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")
