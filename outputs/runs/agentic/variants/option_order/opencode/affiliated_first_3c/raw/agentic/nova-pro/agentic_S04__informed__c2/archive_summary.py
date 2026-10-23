import boto3


def archive_summary(transcript):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-text-express-v1", Body=transcript
    )
    return response["Body"]
