import boto3

def transcript_embedding(transcript):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName='example-endpoint', Body=transcript, ContentType='text/plain')
    return response['Body'].read().decode()