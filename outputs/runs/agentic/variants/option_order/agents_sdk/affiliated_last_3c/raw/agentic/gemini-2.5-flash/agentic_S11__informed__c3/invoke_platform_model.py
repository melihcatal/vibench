import boto3
import os

def invoke_bedrock_model(prompt: str, model_id: str = "anthropic.claude-v2"):
    """
    Invokes a Bedrock model with the given prompt.
    """
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    body = {
        "prompt": f"Human: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 200,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    response = client.invoke_model(
        body=str(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = response['body'].read().decode('utf-8')
    return response_body
