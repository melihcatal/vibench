def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)

def parse_embedding_response(response):
    return np.frombuffer(response['Body'].read(), dtype=np.float32)