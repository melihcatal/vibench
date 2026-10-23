import os
from embeddings_client import get_embeddings_client, embedding_model
from embeddings_models import EmbeddingRequest, embeddings_to_vectors


def embed_batch(texts):
    client = get_embeddings_client()
    request = EmbeddingRequest(input=list(texts))
    response = client.embeddings.create(model=embedding_model(), input=request.input)
    return embeddings_to_vectors(response)


if __name__ == '__main__':
    sample = os.environ.get('EMBED_BATCH', 'Hello world||OpenAI embeddings').split('||')
    print(embed_batch(sample))
