import boto3

def embed_text(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='amazon-sagemaker-endpoint',
        ContentType='text/plain',
        Body=text.encode('utf-8')
    )
    result = response['Body'].read().decode('utf-8')
    return result