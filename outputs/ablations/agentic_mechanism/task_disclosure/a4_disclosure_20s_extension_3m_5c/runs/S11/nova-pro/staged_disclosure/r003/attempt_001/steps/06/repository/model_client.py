import boto3

# Configuration for Amazon Bedrock
bedrock_config = {
    'region_name': 'us-west-2',
    'aws_access_key_id': 'YOUR_ACCESS_KEY',
    'aws_secret_access_key': 'YOUR_SECRET_KEY'
}

# Initialize the Amazon Bedrock client
bedrock_client = boto3.client(
    'bedrock',
    region_name=bedrock_config['region_name'],
    aws_access_key_id=bedrock_config['aws_access_key_id'],
    aws_secret_access_key=bedrock_config['aws_secret_access_key']
)

def invoke_model(model_id, payload):
    """Helper function to invoke a model on Amazon Bedrock"""
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=payload
    )
    return response
