import os
import json
from typing import Iterator, Dict, Any

import boto3
from botocore.exceptions import ClientError


def stream_bedrock_generation(
    model_id: str, prompt: str, inference_parameters: Optional[Dict[str, Any]] = None
) -> Iterator[Dict[str, Any]]:
    """
    Stream output from a Bedrock model invocation.
    Yields chunks of the response as they arrive.
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
        response = client.invoke_model_with_response_stream(
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

        for event in response["body"]:
            chunk = json.loads(event["chunk"]["bytes"].decode("utf-8"))
            yield {"chunk": chunk, "model_id": model_id}
    except ClientError as e:
        raise Exception(f"Failed to stream model {model_id}: {e}")
