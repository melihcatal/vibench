import boto3


def embed_text(text):
    bedrock = boto3.client("bedrock-runtime")
    result = bedrock.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return result
