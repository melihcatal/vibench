import os

import boto3


def platform_output_embedding(text: str):
    client = boto3.client("bedrock-runtime")
    return client.invoke_model(
        modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1"),
        body=f'{{"inputText":"{text}"}}',
    )
