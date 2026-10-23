import boto3

sagemaker = boto3.client('sagemaker')

def transcript_embedding(text):
    response = sagemaker.invoke_endpoint(
        EndpointName='example-endpoint',
        ContentType='text/plain',
        Body=text
    )
    return response['Body'].read()