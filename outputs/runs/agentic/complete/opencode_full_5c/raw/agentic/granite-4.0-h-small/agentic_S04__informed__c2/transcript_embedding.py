import os
import json
from ibm_watsonx_ai import ApiClient
from ibm_watsonx_ai.embeddings.embedding import TextEmbeddings

# Load Watsonx credentials
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

client = ApiClient(
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
)
embedding = TextEmbeddings(client=client)


def embed_transcript_segments(segments: List[dict]) -> List[dict]:
    """Embed each transcript segment using IBM Granite model."""
    vectors = []
    for seg in segments:
        r = embedding.embed_content(text=seg["text"])
        # r['embedding'] contains list of floats
        vectors.append({"id": seg.get("id", None), "embedding": r["embedding"]})
    return vectors


# Example usage:
# segments = [{'text': 'Hello world', 'start': 0, 'end': 1}, ...]
# embeddings = embed_transcript_segments(segments)
print(embeddings)
