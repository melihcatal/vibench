import boto3
import os

def invoke_model(prompt: str, model_id: str = "anthropic.claude-v2"):
    """
    Invokes a provider-managed model (AWS Bedrock) through a platform client.
    """
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    body = {
        "prompt": f"Human: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 200,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    return response_body["completion"]
