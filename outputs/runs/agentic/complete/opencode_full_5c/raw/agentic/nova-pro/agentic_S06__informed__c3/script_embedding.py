import os
import boto3

# Set up the Amazon Titan Embeddings client
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

client = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)


def embed_script(script):
    response = client.invoke_model(
        model_id="amazon.titan-embed-text-v1", body={"inputText": script}
    )
    return response["embedding"]
