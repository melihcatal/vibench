import boto3


def transcript_embedding(text: str) -> dict:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="cohere.embed-english-v3",
        body=("{\"texts\":[\"" + text.replace('"', '\\"') + "\"],\"input_type\":\"search_document\"}" ).encode(),
        contentType="application/json",
        accept="application/json",
    )
    return response
