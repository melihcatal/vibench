import boto3


def transcript_embedding(transcript):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=transcript
    )
    return response["Body"]
