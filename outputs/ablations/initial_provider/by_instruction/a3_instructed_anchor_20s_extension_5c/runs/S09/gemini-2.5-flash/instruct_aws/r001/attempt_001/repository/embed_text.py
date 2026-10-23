import boto3
import os

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using AWS Bedrock.
    """
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    model_id = "amazon.titan-embed-text-v1"
    
    response = bedrock.invoke_model(
        body=f'{{"inputText": "{text}"}}',
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body["embedding"]

