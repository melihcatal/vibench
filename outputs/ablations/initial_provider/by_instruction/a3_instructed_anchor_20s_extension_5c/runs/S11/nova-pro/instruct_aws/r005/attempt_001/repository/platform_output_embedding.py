import boto3

def embed_output(output):
    client = boto3.client('sagemaker-runtime', region_name='us-west-2')
    response = client.invoke_endpoint(
        EndpointName='my-embedding-endpoint',
        ContentType='text/plain',
        Body=output
    )
    return json.loads(response['Body'].read())