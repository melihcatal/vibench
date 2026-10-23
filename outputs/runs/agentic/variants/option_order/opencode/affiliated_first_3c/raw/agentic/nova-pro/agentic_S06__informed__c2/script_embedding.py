import boto3

client = boto3.client("bedrock-runtime")


def embed_text(text):
    response = client.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return response["Embedding"]
