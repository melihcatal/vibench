import boto3
import os
import json

def collect_bedrock_metadata(
    model_id: str,
    body: dict,
    content_type: str = "application/json",
    accept: str = "application/json",
) -> dict:
    """
    Invokes an AWS Bedrock model and returns its output together with provider platform metadata.

    Args:
        model_id (str): The ID of the model to invoke.
        body (dict): The request body for the model invocation.
        content_type (str): The content type of the request body.
        accept (str): The accept header for the response.

    Returns:
        dict: Model output along with platform metadata.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    response = client.invoke_model(
        modelId=model_id,
        contentType=content_type,
        accept=accept,
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    
    # Extract metadata. The exact structure depends on the model.
    # For this example, we'll return a simplified metadata structure.
    metadata = {
        "ResponseContentType": response["ResponseContentType"],
        "BedrockModelArn": response["BedrockModelArn"],
        "Usage": response_body.get("usage", {}), # Assuming 'usage' might be in the response body
        "ModelOutput": response_body
    }

    return metadata
