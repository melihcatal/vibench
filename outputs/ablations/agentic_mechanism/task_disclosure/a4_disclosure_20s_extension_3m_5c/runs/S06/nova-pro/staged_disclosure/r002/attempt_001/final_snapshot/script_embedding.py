import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_script(script_text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': script_text
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

# Example usage
script_text = 'This is a narration script for a voice-asset search.'
embedding = embed_script(script_text)
print(embedding)