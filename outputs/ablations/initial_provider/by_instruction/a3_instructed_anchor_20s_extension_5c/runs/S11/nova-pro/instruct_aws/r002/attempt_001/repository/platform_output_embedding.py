import boto3

def embed_output(response):
    client = boto3.client('sagemaker-runtime', region_name='us-west-2')
    endpoint_name = 'huggingface-pytorch-inference-2023-07-26-17-09-07-310'
    text = response['body']['completion']
    payload = {'inputs': text}
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(payload)
    )
    return json.loads(response['Body'].read())