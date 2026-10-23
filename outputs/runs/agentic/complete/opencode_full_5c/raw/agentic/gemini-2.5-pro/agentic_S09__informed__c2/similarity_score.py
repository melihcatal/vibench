import numpy as np
from embeddings_client import client
from embeddings_models import SimilarityRequest, SimilarityResponse


def similarity_score(request: SimilarityRequest) -> SimilarityResponse:
    texts_to_embed = [request.text1, request.text2]
    response = client.embeddings.create(
        input=texts_to_embed, model="text-embedding-3-small"
    )

    embedding1 = np.array(response.data[0].embedding)
    embedding2 = np.array(response.data[1].embedding)

    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    cosine_similarity = dot_product / (norm1 * norm2)

    return SimilarityResponse(score=float(cosine_similarity))
