import boto3
import os

bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def summarize_meeting(transcript):
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-text-express-v1", Body=transcript
    )
    return response["Body"].read().decode("utf-8")
