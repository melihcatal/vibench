import boto3


def embed_log_message(log_text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1", body={"inputText": log_text}
    )
    return response["embedding"]
