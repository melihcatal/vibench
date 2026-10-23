import boto3


def embed_sections(sections):
    client = boto3.client("bedrock-runtime")
    payload = {"inputText": "
".join(sections)}
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=str(payload).encode("utf-8"), contentType="application/json", accept="application/json")
    return response
