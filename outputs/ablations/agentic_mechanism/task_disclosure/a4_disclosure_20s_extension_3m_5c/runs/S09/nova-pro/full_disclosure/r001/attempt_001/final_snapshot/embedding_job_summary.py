import boto3

def summarize_embedding_job_results(job_results):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    payload = {
        'inputText': job_results,
        'textEmbeddingsConfig': {
            'strategy': 'AVERAGE'
        }
    }
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result['embedding']