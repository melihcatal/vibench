import boto3

def extract_fields(text, config=None):
    config = config or {}
    client = boto3.client('lambda', region_name=config.get('region'))
    response = client.invoke(FunctionName='extract_fields_function', InvocationType='RequestResponse', Payload=text)
    return response['Payload'].read()