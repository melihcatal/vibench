import boto3


def platform_output_embedding(text: str):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=f'{{"inputText":"{text.replace("\\", "\\\\").replace('"', '\\"')}"}}',
        accept="application/json",
        contentType="application/json",
    )
    return response["body"].read()
