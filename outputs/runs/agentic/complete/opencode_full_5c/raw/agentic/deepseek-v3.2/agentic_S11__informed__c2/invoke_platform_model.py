import boto3
import json
from typing import Dict, Any


def invoke_bedrock_model(
    model_id: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Invoke a provider-managed model through Amazon Bedrock.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"],
        }
    )

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    response_body = json.loads(response["body"].read())
    return response_body
