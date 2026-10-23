import boto3
import numpy as np

def get_embedding(text):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embedding = response['embedding']
    return np.array(embedding)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def compute_similarity(text1, text2):
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return cosine_similarity(embedding1, embedding2)