import boto3

lambda_client = boto3.client('lambda')

def embed_text(text):
    response = lambda_client.invoke(
        FunctionName='text-embedding-function',
        InvocationType='RequestResponse',
        Payload=text
    )
    return response['Payload'].read()