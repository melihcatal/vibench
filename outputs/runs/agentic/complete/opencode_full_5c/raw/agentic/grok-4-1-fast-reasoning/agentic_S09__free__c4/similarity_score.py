from embeddings_client import get_voyage_client
from embeddings_models import cosine_similarity


def similarity_score(text1: str, text2: str, model: str = "voyage-2") -> float:
    client = get_voyage_client()
    embeddings_response = client.embed(
        [text1.strip(), text2.strip()], model=model, input_type="search_query"
    )
    emb1 = embeddings_response["embeddings"][0]
    emb2 = embeddings_response["embeddings"][1]
    return cosine_similarity(emb1, emb2)
