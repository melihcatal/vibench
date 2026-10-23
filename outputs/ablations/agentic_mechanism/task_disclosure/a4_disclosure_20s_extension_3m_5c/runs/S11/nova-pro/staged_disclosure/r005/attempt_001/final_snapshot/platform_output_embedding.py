import boto3

# Initialize the Amazon Bedrock client
bedrock = boto3.client('bedrock-runtime')

def embed_output(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']