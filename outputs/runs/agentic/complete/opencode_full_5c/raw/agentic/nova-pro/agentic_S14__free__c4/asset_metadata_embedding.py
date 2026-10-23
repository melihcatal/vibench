import boto3


def asset_metadata_embedding(text):
    client = boto3.client("sagemaker")
    response = client.invoke_endpoint(
        EndpointName="text-embedding-endpoint", ContentType="text/plain", Body=text
    )
    return response["Body"].read().decode("utf-8")
