# [SAME-SCENARIO] stream_platform_generation.py

# Stream generation from a Bedrock model while preserving raw response objects
import os
import json
from boto3 import client as boto3_client
from io import StringIO

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

bedrock = boto3_client(
    "bedrock",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def stream_generation(model_id: str, prompt: str, chunk_size: int = 1024):
    """Yield incremental chunks of model output while streaming.

    Args:
        model_id: Bedrock model ARN.
        prompt: Text prompt to the model.
        chunk_size: Bytes to read per chunk (affects granularity).

    Yields:
        tuple: (raw_chunk: bytes, response_obj: dict) for each received chunk.
    """
    payload = {
        "inputs": [{"content": prompt, "contentType": "text/plain"}],
        "parameters": {"maxTokens": 2048, "stream": True, "temperature": 0.7},
    }
    # Bedrock streaming endpoint expects a multipart request; use low‑level client
    response = bedrock.invoke_endpoint(
        ModelId=model_id, ContentType="application/json", Body=json.dumps(payload)
    )
    stream = response["Body"]
    buffer = bytearray()
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        buffer.extend(chunk)
        # Emit a chunk only when a newline is encountered (model token boundary)
        if b"\n" in buffer:
            lines = buffer.split(b"\n")
            for line in lines[:-1]:
                yield (
                    line + b"\n",
                    json.loads(response["Body"].read().decode()),
                )  # reuse first response object for simplicity
            buffer = lines[-1]
    # Yield any remaining buffered data
    if buffer:
        yield buffer, json.loads(response["Body"].read().decode())
