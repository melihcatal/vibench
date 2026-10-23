import boto3
import os

def invoke_bedrock_model(
    model_id: str,
    body: dict,
    content_type: str = "application/json",
    accept: str = "application/json",
) -> dict:
    """
    Invokes a provider-managed model through AWS Bedrock.

    Args:
        model_id (str): The ID of the model to invoke.
        body (dict): The request body for the model invocation.
        content_type (str): The content type of the request body.
        accept (str): The accept header for the response.

    Returns:
        dict: The response from the model invocation.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    response = client.invoke_model(
        modelId=model_id,
        contentType=content_type,
        accept=accept,
        body=str(body) # Bedrock expects a string for the body
    )
    
    response_body = response["body"].read().decode("utf-8")
    return {"statusCode": 200, "body": response_body}
