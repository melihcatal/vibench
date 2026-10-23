import boto3

bedrock = boto3.client('bedrock-runtime')

def generate_embeddings(texts):
    model_id = 'amazon.titan-embed-text-v1'
    embeddings = []
    for text in texts:
        response = bedrock.invoke_model(
            modelId=model_id,
            body={
                'inputText': text
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings