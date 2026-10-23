import boto3


def embed_platform_output(output):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=b'{ "input_text": "' + output + '" }'
    )
    return response
