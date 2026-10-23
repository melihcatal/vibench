from embeddings_client import embedding_model, get_client
from embeddings_models import normalize_vector


def embed_text(text: str):
    response = get_client().embeddings.create(model=embedding_model(), input=text)
    return normalize_vector(response.data[0].embedding)


if __name__ == "__main__":
    print(embed_text("OpenAI embeddings are useful."))
