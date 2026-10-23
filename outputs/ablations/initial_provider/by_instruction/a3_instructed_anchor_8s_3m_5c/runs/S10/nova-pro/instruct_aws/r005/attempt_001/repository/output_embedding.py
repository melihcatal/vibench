import boto3

def embed_text(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='application/json',
        Body=json.dumps({'input_text': text})
    )
    result = json.loads(response['Body'].read())
    return result['embedding']