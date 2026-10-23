import boto3

def embed_log_message(log_message):
    client = boto3.client('sagemaker-runtime', region_name='us-west-2')
    response = client.invoke_endpoint(
        EndpointName='my-log-embedding-endpoint',
        ContentType='text/plain',
        Body=log_message
    )
    return response['Body'].read()