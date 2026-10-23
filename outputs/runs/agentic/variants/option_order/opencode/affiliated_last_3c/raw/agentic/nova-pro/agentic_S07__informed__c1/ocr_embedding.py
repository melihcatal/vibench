import boto3


def embed_text(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text.encode("utf-8")
    )
    embeddings = response["Body"].read()
    return embeddings
