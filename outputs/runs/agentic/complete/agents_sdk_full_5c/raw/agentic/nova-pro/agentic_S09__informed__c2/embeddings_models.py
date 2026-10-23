def normalize_embedding(embedding):
    return np.array(embedding) / np.linalg.norm(embedding)

def format_response(response):
    return [item.embedding for item in response.data]