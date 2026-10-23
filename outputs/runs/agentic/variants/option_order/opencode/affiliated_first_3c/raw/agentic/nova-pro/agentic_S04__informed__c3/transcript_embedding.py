import boto3

bedrock_client = boto3.client("bedrock-runtime")


def transcript_embedding(text):
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    return response["Embedding"]
