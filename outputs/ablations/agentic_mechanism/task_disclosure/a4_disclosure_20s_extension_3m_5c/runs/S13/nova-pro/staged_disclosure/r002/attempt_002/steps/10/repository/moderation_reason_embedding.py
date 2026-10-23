import boto3

def embed_moderation_rationale(rationale):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': rationale
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']