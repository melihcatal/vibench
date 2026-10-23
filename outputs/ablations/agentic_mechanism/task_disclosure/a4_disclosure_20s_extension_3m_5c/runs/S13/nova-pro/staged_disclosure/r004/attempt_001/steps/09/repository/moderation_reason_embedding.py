import boto3

bedrock = boto3.client('bedrock-runtime')

def generate_embedding(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': text
    }
    response = bedrock.invoke_model(
        modelId=model_id,
        body=body
    )
    result = json.loads(response['body'].read())
    return result['embedding']

# Example usage
rationale = 'This content violates community guidelines.'
embedding = generate_embedding(rationale)
print(embedding)