import boto3
import os
import json

def stream_bedrock_generation(prompt: str, model_id: str = "anthropic.claude-v2"):
    """
    Streams output from a Bedrock model, yielding chunks as they are received.
    """
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    body = {
        "prompt": f"Human: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 500,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop_sequences": ["\n\nHuman:"]
    }

    response = client.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    for event in response['body']:
        chunk = event.get('chunk')
        if chunk:
            yield json.loads(chunk.get('bytes').decode('utf-8'))['completion']
