import os
from openai import OpenAI
from embeddings_client import get_embeddings_client, embedding_model
from embeddings_models import EmbeddingRequest, first_embedding, vector_to_list


def embed_text(text: str):
    client = get_embeddings_client()
    request = EmbeddingRequest(input=text)
    response = client.embeddings.create(model=embedding_model(), input=request.input)
    return vector_to_list(first_embedding(response).embedding)


if __name__ == '__main__':
    print(embed_text(os.environ.get('EMBED_TEXT', 'Hello world')))
