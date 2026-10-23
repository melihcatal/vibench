import boto3


def embed_document_sections(text):
    bedrock_runtime_client = boto3.client("bedrock-runtime")
    response = bedrock_runtime_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    embeddings = response["Body"].read()
    return embeddings
