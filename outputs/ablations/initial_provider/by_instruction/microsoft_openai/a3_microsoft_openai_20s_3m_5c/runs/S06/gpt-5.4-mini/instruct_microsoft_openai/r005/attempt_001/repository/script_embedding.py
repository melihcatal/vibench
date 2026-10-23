from speech_client import embedding_client


def embed_script(text):
    response = embedding_client().embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
