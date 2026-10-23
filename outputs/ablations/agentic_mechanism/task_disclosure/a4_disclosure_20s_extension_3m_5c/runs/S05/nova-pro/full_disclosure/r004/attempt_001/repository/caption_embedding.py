import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_caption(caption):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': caption
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']
