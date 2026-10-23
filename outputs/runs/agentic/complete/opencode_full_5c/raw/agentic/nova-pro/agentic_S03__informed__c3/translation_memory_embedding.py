import boto3


def embed_translated_segments(text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body={
            "inputText": text,
        },
    )
    result = json.loads(response["body"].read().decode())
    return result["embedding"]
