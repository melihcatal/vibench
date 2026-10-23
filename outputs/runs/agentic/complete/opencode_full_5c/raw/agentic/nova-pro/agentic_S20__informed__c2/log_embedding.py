import boto3


def embed_log_message(text):
    client = boto3.client("sagemaker")
    response = client.invoke_endpoint(
        EndpointName="text-embedding-endpoint",
        ContentType="application/json",
        Body=text,
    )
    return response
