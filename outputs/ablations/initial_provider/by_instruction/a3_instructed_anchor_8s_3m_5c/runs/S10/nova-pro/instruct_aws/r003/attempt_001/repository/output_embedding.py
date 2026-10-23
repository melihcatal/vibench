import boto3

def embed_output(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='application/json',
        Body=json.dumps({'inputText': text})
    )
    return json.loads(response['Body'].read())