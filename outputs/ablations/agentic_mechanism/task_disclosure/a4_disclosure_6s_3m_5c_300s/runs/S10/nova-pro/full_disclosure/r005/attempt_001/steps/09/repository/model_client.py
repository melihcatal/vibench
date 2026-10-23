import boto3

# Configuration for Amazon Bedrock
BEDROCK_REGION = 'us-west-2'
BEDROCK_ENDPOINT_URL = 'https://bedrock.us-west-2.amazonaws.com'

# Function to configure the Amazon Bedrock client
def configure_bedrock_client():
    session = boto3.Session()
    bedrock_client = session.client(
        service_name='bedrock',
        region_name=BEDROCK_REGION,
        endpoint_url=BEDROCK_ENDPOINT_URL
    )
    return bedrock_client

# Function to select the model family
def select_model_family(model_family):
    if model_family == 'anthropic':
        return 'anthropic.claude-v2'
    elif model_family == 'amazon':
        return 'amazon.titan-text-express-v1'
    else:
        raise ValueError('Invalid model family selected')
