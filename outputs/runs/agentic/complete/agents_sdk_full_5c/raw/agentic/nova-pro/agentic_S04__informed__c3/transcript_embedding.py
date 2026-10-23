import boto3

bedrock_client = boto3.client('bedrock-runtime')

def embed_transcript(transcript_text):
    model_id = 'amazon.titan-embed-text-v1'
    payload = {'inputText': transcript_text}
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload)
    )
    result = json.loads(response['body'].read().decode())
    return result['embedding']