import os
import cohere
from model_models import EmbeddingResult


def platform_output_embedding(text: str) -> EmbeddingResult:
    client = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
    response = client.embed(
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"],
        texts=[text],
    )
    vector = response.embeddings.float_[0]
    return EmbeddingResult(
        vector=vector,
        model="embed-english-v3.0",
        dimensions=len(vector),
        raw_response=response,
    )
