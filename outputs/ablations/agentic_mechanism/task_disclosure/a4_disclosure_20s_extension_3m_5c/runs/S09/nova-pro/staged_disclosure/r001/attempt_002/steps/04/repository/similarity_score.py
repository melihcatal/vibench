import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def compute_similarity(text1, text2):
    try:
        bedrock = boto3.client('bedrock-runtime')

        # Generate embeddings for the texts
        response1 = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text1
            }
        )
        response2 = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text2
            }
        )

        # Extract the embeddings from the responses
        embedding1 = response1['embedding']
        embedding2 = response2['embedding']

        # Compute the cosine similarity between the embeddings
        import numpy as np
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

        return similarity

    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

# Example usage:
# text1 = 'This is the first text.'
# text2 = 'This is the second text.'
# similarity = compute_similarity(text1, text2)
# print(f'Cosine similarity: {similarity}')
