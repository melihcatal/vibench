import boto3

def embed_text(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='amazon-sagemaker-endpoint-id',
        ContentType='text/plain',
        Body=text.encode('utf-8')
    )
    result = response['Body'].read()
    return result