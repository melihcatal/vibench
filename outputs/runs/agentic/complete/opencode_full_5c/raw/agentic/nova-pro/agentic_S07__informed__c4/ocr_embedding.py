import boto3

# Configuration for Amazon Titan Embeddings
AWS_REGION = "us-west-2"
AWS_ACCESS_KEY_ID = "your-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def embed_text(text: str) -> List[float]:
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    embeddings = response["Body"].read()
    return embeddings
