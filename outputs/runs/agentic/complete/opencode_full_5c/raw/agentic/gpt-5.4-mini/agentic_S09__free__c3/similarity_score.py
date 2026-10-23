from embeddings_client import embedding_model, get_client
from embeddings_models import cosine_similarity


def similarity_score(left_text: str, right_text: str) -> float:
    response = get_client().embeddings.create(
        model=embedding_model(), input=[left_text, right_text]
    )
    return cosine_similarity(response.data[0].embedding, response.data[1].embedding)


if __name__ == "__main__":
    print(similarity_score("cat", "feline"))
