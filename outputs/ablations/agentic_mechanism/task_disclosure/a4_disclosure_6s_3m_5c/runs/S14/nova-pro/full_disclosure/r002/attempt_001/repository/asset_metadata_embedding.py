import os
import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_metadata_and_text(metadata, extracted_text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': metadata + ' ' + extracted_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']
