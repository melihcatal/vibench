import boto3
import os
import json

def embed_with_amazon_titan(text: str, model_id: str = "amazon.titan-embed-text-v1"):
    """
    Generates embeddings for a given text using Amazon Titan Embeddings via Bedrock Runtime.
    """
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    body = json.dumps({"inputText": text})
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body.get('embedding')
