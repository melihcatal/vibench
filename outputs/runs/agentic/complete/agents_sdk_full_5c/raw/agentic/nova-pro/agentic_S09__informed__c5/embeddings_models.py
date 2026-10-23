from cohere import EmbedResponse

def normalize_embedding(embedding):
    return [float(e) for e in embedding]

def parse_embed_response(response: EmbedResponse):
    return [normalize_embedding(e) for e in response.embeddings]