import boto3

def compute_cosine_similarity(embedding1, embedding2):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': embedding1,
            'targetText': embedding2
        }
    )
    similarity_score = response['similarityScore']
    return similarity_score