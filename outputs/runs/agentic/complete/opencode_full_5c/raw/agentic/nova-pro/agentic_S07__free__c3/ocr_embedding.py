import sagemaker


def embed_text(text):
    sagemaker_client = boto3.client("sagemaker")
    response = sagemaker_client.invoke_endpoint(
        EndpointName="text-embedding-endpoint", Body=text
    )
    return response["Body"].read()
