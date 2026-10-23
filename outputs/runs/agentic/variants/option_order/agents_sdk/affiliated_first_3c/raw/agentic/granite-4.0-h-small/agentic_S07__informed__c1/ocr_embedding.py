import boto3

# Embeddings using Amazon Bedrock Titan Text Embeddings (example for English)
bedrock_client = boto3.client('bedrock-runtime')

MODEL_ID = 'amazon.titan-text-embed-v1'

def embed_text(text: str) -> List[float]:
    '''Embed extracted document sections using Amazon Titan embeddings.'''
    response = bedrock_client.invoke_model(
        ModelId=MODEL_ID,
        ContentType='application/json',
        Body=text.encode('utf-8')
    )
    payload = response['Body'].read().decode('utf-8')
    # Expected JSON format: [{"embedding": [0.1,0.2,...]}, ...]
    embeddings = json.loads(payload)
    # Return the first embedding vector for the whole text (simple approach)
    return embeddings[0]['embedding']

# For alternative providers, you could switch to openai, google, etc.
# e.g., openai_client = openai.OpenAI()
# def embed_openai(text: str):
#     return openai_client.embeddings.create(input=text, model='text-embedding-ada-2')['data'][0]['embedding']
