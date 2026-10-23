import boto3
import json

def embed_log_message(log_message):
    bedrock = boto3.client('bedrock-runtime')
    payload = {
        'inputText': log_message,
        'textEmbeddingModelId': 'amazon.titan-embed-text-v1'
    }
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId='amazon.titan-embed-text-v1',
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response['body'].read())
    embedding = response_body['embedding']
    return embedding

if __name__ == '__main__':
    log_message = 'Example log message to embed'
    embedding = embed_log_message(log_message)
    print(f'Embedding: {embedding}')
