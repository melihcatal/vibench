import boto3
import json
from model_client import get_bedrock_client

def collect_bedrock_metadata(
    prompt: str,
    model_id: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> dict:
    """
    Invokes an AWS Bedrock model and returns its output along with provider platform metadata.
    """
    client = get_bedrock_client()

    body = json.dumps({
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens_to_sample": max_tokens
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    
    # In a real scenario, more specific metadata might be extracted from response headers
    # or other parts of the response object, depending on the model and API.
    # For Bedrock, some metadata might be implicitly part of the response structure.
    metadata = {
        "model_id": model_id,
        "response_headers": response["ResponseMetadata"] # Example of capturing some metadata
    }

    return {
        "generated_text": response_body.get("completion"),
        "metadata": metadata
    }
