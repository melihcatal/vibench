import boto3

def embed_caption_chunks(caption_chunks):
    bedrock = boto3.client('bedrock-runtime')
    embeddings = []
    for chunk in caption_chunks:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': chunk
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings