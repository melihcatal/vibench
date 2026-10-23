import boto3


def embed_script(script):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=script
    )
    return response["Embedding"]
