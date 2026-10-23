import boto3


def stream_generation():
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-text-express-v1", body='{"inputText": "Hello, world!"}'
    )
    yield response
