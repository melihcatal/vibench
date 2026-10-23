import boto3

# Set up the Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Function to embed text
def embed_text(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': text
    }
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    result = json.loads(response['body'].read())
    return result['embedding']
