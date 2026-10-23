import boto3

# Initialize the Amazon Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

# Function to embed text using Amazon Bedrock
def embed_text(text):
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = response['body'].read()
    embeddings = json.loads(result)['embedding']
    return embeddings

# Example usage
query = 'example query'
documents = ['example document 1', 'example document 2']

query_embedding = embed_text(query)
document_embeddings = [embed_text(doc) for doc in documents]

print('Query embedding:', query_embedding)
print('Document embeddings:', document_embeddings)