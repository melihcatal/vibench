import os
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def embed_log(text):
    response = bedrock.invoke_model(
        model_id="amazon.titan-embed-text-v1", body={"inputText": text}
    )
    return response["embedding"]
