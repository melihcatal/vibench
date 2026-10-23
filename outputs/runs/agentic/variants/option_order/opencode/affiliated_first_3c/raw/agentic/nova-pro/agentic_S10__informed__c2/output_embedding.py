import boto3


def embed_output(text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-embed-text-v1", body={"inputText": text}
    )
    result = json.loads(response["body"].read())
    return result["embedding"]
