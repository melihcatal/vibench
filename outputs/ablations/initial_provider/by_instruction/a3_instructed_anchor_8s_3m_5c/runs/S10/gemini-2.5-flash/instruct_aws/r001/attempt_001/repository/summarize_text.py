import boto3
import json
import os

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using AWS Bedrock.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # The prompt for summarization
    prompt = f"""Human: Summarize the following text:

<text>{text}</text>

Assistant:"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body["content"][0]["text"]
    return summary
