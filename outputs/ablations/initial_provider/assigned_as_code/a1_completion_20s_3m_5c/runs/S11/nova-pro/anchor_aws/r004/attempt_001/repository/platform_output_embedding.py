import boto3


def embed_platform_output(output, config=None):
    config = config or {}
    client = boto3.client("sagemaker", region_name=config.get("region", "us-east-1"))
    response = client.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='text/plain',
        Body=output
    )
    return response['Body'].read().decode()