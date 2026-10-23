import boto3

def embed_text(text, config=None):
    config = config or {}
    client = boto3.client('lambda', region_name=config.get('region'))
    response = client.invoke(FunctionName='embed_text_function', InvocationType='RequestResponse', Payload=text)
    return response['Payload'].read()