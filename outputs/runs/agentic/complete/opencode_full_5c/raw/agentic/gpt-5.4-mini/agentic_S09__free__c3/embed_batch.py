from embeddings_client import embedding_model, get_client
from embeddings_models import normalize_vector


def embed_batch(texts):
    response = get_client().embeddings.create(
        model=embedding_model(), input=list(texts)
    )
    return [normalize_vector(item.embedding) for item in response.data]


if __name__ == "__main__":
    print(embed_batch(["first", "second"]))
