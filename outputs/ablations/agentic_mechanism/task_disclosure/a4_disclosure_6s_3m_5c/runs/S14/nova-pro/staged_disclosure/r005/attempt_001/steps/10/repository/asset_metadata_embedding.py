import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def embed_metadata(metadata):
    # Convert metadata to text representation
    metadata_text = str(metadata)
    return embed_text(metadata_text)