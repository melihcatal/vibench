import os
from typing import Optional, Dict, Any

import boto3
from botocore.exceptions import ClientError


def get_bedrock_client():
    """Initialize and return a Bedrock Runtime client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def invoke_model(
    model_id: str, prompt: str, inference_parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Invoke a Bedrock model with the given prompt and parameters."""
    client = get_bedrock_client()

    if inference_parameters is None:
        inference_parameters = {}

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=bytes(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {**inference_parameters},
                }.__str__(),
                "utf-8",
            ),
        )
        return {
            "body": response["body"].read().decode("utf-8"),
            "content_type": response["contentType"],
        }
    except ClientError as e:
        raise Exception(f"Failed to invoke model {model_id}: {e}")
