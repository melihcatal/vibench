import boto3
import json
from model_client import BedrockClient
from model_models import ModelInvocationRequest, ModelStreamResponse
from typing import Iterator

def stream_bedrock_generation(request: ModelInvocationRequest) -> Iterator[ModelStreamResponse]:
    """
    Streams output from a managed model platform (AWS Bedrock) while preserving provider response objects.
    """
    client = BedrockClient().get_client()

    body = json.dumps({
        "prompt": request.prompt,
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature
    })

    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json"
    )

    stream = response.get('body')

    for event in stream:
        if "chunk" in event:
            chunk = event.get("chunk")
            if chunk:
                chunk_bytes = chunk.get("bytes")
                if chunk_bytes:
                    # Decode the bytes to string and then parse as JSON
                    chunk_data = json.loads(chunk_bytes.decode('utf-8'))
                    yield ModelStreamResponse(
                        chunk_text=chunk_data.get('completion'),
                        raw_provider_response=chunk_data # Preserve the raw chunk data
                    )
