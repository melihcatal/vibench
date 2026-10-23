import boto3

bedrock_client = boto3.client('bedrock-runtime')

def summarize_transcript(transcript_text):
    model_id = 'amazon.titan-text-express-v1'
    payload = {
        'inputText': transcript_text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0,
            'topP': 0.9
        }
    }
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload)
    )
    result = json.loads(response['body'].read().decode())
    return result['results'][0]['outputText']