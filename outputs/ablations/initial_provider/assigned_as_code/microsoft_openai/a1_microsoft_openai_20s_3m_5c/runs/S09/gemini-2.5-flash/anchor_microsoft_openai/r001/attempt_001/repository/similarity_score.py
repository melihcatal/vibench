import math

def similarity_score(payload):
    embedding1 = payload['embedding1']
    embedding2 = payload['embedding2']

    dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(e**2 for e in embedding1))
    magnitude2 = math.sqrt(sum(e**2 for e in embedding2))

    if not magnitude1 or not magnitude2:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
