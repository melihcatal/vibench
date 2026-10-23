import boto3
import os
import json

def invoke_bedrock_model(prompt: str, model_id: str = "anthropic.claude-v2"):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.5,
    })
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # export AWS_SECRET_ACCESS_KEY="your-secret-key"
    prompt_text = "Hello, what is the capital of France?"
    result = invoke_bedrock_model(prompt_text)
    print(f"Model response: {result}")
