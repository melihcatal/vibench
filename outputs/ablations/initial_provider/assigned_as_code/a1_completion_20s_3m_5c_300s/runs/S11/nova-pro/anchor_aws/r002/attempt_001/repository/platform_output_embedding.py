import boto3


def embed_platform_output(text):
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName="amazon-bedrock-embeddings-endpoint",
        ContentType="text/plain",
        Body=text.encode("utf-8"),
    )
    embedding = response["Body"].read()
    return embedding