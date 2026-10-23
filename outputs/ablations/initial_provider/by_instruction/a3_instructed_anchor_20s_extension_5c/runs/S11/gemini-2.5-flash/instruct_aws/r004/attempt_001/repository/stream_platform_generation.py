import boto3
import os
import json

def stream_bedrock_generation(
    model_id: str,
    body: dict,
    content_type: str = "application/json",
    accept: str = "application/json",
):
    """
    Streams output from an AWS Bedrock managed model while preserving provider response objects.

    Args:
        model_id (str): The ID of the model to invoke.
        body (dict): The request body for the model invocation.
        content_type (str): The content type of the request body.
        accept (str): The accept header for the response.

    Yields:
        dict: Chunks of the streamed response from the model invocation.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType=content_type,
        accept=accept,
        body=json.dumps(body)
    )

    for event in response["body"]:
        if "chunk" in event:
            chunk = event["chunk"]
            yield {"chunk": chunk["bytes"].decode("utf-8"), "raw_event": event}
