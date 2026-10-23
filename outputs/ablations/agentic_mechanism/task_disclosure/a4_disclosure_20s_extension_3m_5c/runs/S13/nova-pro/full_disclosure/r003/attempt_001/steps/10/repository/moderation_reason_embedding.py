import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_moderation_rationales(rationales):
    embeddings = []
    for rationale in rationales:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': rationale
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings