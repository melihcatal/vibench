import json
import os
from google.cloud import genai
from model_models import PromptResponse

# ---------------------------------------------------------------------------
# Example: Vertex AI / Gemini Embedding integration (Google Cloud)
# ---------------------------------------------------------------------------

# Set GOOGLE_APPLICATION_CREDENTIALS env var to a service account JSON
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var for Google Cloud")

# Initialize GenAI client
genai.configure()
client = genai.Service()   # high‑level client for Vertex AI services

# Use the Gemini embeddings model (embed‑2184‑text‑embedding‑3‑google‑cloud)
EMBEDDING_MODEL = "embed-184b-text-embedding-3-google-cloud"


def create_embedding(response: PromptResponse) -> PromptResponse:
    """Generate an embedding for the generated text and attach it to the response."""
    # Vertex AI expects a list of documents, each with a content field
    docs = [{"content": response.generated_text}]
    embeddings = client.embeddings.predict(docs, model=EMBEDDING_MODEL)
    # embeddings.result() returns a list of dictionaries with a 'vector' key
    vector = embeddings.result()[0].get('vector')
    enriched = response._replace(
        raw=json.loads(embeddings.to_string()) if embeddings.to_string() else {},
        usage_info={"embedding": {"model": EMBEDDING_MODEL, "vector_dim": len(vector)}}
    )
    # Store the vector as a JSON‑encoded list for persistence
    enriched.raw["embedding"] = vector
    return enriched

# Quick demo (uncomment to run)
# if __name__ == "__main__":
#     prompt = input("Prompt: ")
#     raw = collect_platform_metadata(prompt)
#     embedded = create_embedding(raw)
#     print('\nEmbedding vector size:', len(embedded.raw['embedding']))