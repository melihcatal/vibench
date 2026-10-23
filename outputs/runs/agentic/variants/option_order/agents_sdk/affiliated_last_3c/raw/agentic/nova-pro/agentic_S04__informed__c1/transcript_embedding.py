import boto3

bedrock = boto3.client('bedrock-runtime')

def transcript_embedding(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    return response['body'].read().decode('utf-8')