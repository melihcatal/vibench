import boto3


def embed_log_message(log_message):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1", body={"inputText": log_message}
    )
    return response["body"]["embedding"]
