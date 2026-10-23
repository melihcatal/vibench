import boto3
from scipy.spatial.distance import cosine

def compute_similarity(text1, text2):
    bedrock = boto3.client('bedrock')
    response1 = bedrock.invoke_model(ModelId='amazon.titan-embed-text-v1', Body=text1)
    response2 = bedrock.invoke_model(ModelId='amazon.titan-embed-text-v1', Body=text2)
    embedding1 = response1['embedding']
    embedding2 = response2['embedding']
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity