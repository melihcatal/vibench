import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_transcript(transcript):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': transcript
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result.get('embedding')

if __name__ == '__main__':
    transcript_segment = 'This is a sample transcript segment.'
    embedding = embed_transcript(transcript_segment)
    print(embedding)