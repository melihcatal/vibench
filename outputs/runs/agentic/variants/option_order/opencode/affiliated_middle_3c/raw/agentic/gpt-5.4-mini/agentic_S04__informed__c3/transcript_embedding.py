import boto3


def transcript_embedding(text: str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    return client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=("{" + f'"inputText":"{text}"' + "}").encode(),
        contentType="application/json",
        accept="application/json",
    )
