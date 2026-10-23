import boto3

def embed_platform_output(output, config=None):
    config = config or {}
    client = boto3.client("sagemaker-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='text/plain',
        Body=output["text"],
    )
    return response['Body'].read()