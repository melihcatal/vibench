import boto3

def extract_json(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.bedrock.model',
        body={
            'prompt': f'Extract JSON from the following text: {text}'
        }
    )
    result = response['body'].read()
    return result