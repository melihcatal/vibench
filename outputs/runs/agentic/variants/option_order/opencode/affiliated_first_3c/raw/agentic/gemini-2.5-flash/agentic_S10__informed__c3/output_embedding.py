import google.generativeai as genai
from model_client import GeminiClient
from model_models import EmbeddingRequest

# Gemini Embeddings: service=Gemini embeddings; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY


def get_embedding(request: EmbeddingRequest) -> dict:
    model = GeminiClient.get_embedding_model()

    # The embedding model is usually specifically for embeddings, not chat completions.
    # The `embed_content` method is used for embedding.
    response = model.embed_content(model=request.model, content=request.text)

    return {"embedding": response["embedding"]}
