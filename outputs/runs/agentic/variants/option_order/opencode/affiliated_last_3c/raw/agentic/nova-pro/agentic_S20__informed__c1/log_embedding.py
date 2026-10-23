import os
import boto3

bedrock = boto3.client("bedrock-runtime")


def embed_log_message(text):
    response = bedrock.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return response["Body"].read()
