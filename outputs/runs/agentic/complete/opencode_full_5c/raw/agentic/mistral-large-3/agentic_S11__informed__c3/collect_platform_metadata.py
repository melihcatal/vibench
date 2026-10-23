import os
import json
from typing import Dict, Any, Tuple

import boto3
from botocore.exceptions import ClientError


def collect_bedrock_metadata(
    model_id: str, prompt: str, inference_parameters: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Invoke a Bedrock model and return the output along with metadata.
    Metadata includes model ID, input tokens, output tokens, and latency.
    """
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    if inference_parameters is None:
        inference_parameters = {}

    try:
        import time

        start_time = time.time()

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

        latency = time.time() - start_time
        response_body = json.loads(response["body"].read().decode("utf-8"))

        metadata = {
            "model_id": model_id,
            "input_tokens": response_body.get("inputTextTokenCount", 0),
            "output_tokens": response_body.get("results", [{}])[0].get("tokenCount", 0),
            "latency": latency,
            "provider": "aws_bedrock",
        }

        return response_body, output_metadata
    except ClientError as e:
        raise Exception(f"Failed to collect metadata for model {model_id}: {e}")
