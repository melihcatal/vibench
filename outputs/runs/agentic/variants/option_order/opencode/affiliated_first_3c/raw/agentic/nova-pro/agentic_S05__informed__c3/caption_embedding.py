import boto3
import os

titan_embeddings_client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def embed_caption(text):
    response = titan_embeddings_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    return response["Body"].read().decode("utf-8")
