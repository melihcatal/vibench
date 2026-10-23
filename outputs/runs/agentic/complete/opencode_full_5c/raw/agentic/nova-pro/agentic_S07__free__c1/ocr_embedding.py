import boto3


def embed_text(text):
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName="text-embedding-endpoint", ContentType="text/plain", Body=text
    )
    return response["Body"].read()
