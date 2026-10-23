# [LATER-STEP] transcript_embedding.py
# Embed transcript segments using IBM Slate embeddings (IBM Watsonx.ai)
import os
from ibm_watsonx_ai import Watsonx
from ibm_watsonx_ai.auth import IAMAuthenticator
from ibm_watsonx_ai.services import Embeddings

authenticator = IAMAuthenticator(apikey=os.getenv("WATSONX_API_KEY"))
client = Watsonx(authenticator=authenticator)
embedding_service = Embeddings(
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    service_url=os.getenv("WATSONX_SERVICE_URL"),
    authenticator=authenticator,
)

def embed_segments(segments: list[dict]) -> list[float]:
    """Return a list of embedding vectors (one per segment text).",
    # Build input list of texts
    texts = [seg["text"] for seg in segments]
    result = embedding_service.embed_documents(texts)
    # Result is a list of dicts with 'embedding' key containing float list
    return [vec["embedding"] for vec in result]

if __name__ == "__main__":
    # Example dummy segment
    sample = [{"text": "Hello world, this is a test of embedding generation."}]
    vectors = embed_segments(sample)
    print("Embeddings:", vectors)
