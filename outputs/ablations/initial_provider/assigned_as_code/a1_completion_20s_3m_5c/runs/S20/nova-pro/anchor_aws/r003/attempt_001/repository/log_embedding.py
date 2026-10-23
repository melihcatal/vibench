import boto3

from observability_client import get_config


def log_embedding(log_message):
    config = get_config()
    client = boto3.client('sagemaker-runtime', region_name=config['region'])
    response = client.invoke_endpoint(
        EndpointName='log-embedding-endpoint',
        ContentType='application/json',
        Body=json.dumps({'inputs': log_message}),
    )
    return json.loads(response['Body'].read())['embedding']