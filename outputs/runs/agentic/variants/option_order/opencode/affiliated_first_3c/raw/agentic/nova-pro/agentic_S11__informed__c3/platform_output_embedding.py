import boto3


def embed_text(text):
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v1", body='{"inputText": "' + text + '"}'
    )
    return response
