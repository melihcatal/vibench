import boto3

def transcript_embedding(transcript):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='MyTranscriptionEndpoint',
        ContentType='text/plain',
        Body=transcript
    )
    return response['Body'].read().decode()