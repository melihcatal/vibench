import boto3


def invoke_model():
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-text-express-v1", body='{"inputText": "Hello, world!"}'
    )
    return response
