import boto3
import json
import os

def summarize_text(text: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    Summarizes the given text using an AWS Bedrock LLM.
    """
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    prompt = f"Human: Summarize the following text:

{text}

Assistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")
