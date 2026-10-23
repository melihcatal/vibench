import boto3


def embed_text(text):
    sagemaker = boto3.client("sagemaker-runtime")
    response = sagemaker.invoke_endpoint(
        EndpointName="text-embedding-endpoint", ContentType="text/plain", Body=text
    )
    return response["Body"].read()
