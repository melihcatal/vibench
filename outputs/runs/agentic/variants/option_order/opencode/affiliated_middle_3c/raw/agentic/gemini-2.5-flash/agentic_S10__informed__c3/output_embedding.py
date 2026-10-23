import os
import google.generativeai as genai
from model_models import EmbeddingRequest, EmbeddingResponse


def get_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embeds model outputs for clustering or retrieval using Gemini Embeddings.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

    try:
        result = genai.embed_content(model=request.model, content=request.text)
        return EmbeddingResponse(embedding=result["embedding"])
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return EmbeddingResponse(embedding={})


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment
    os.environ["GOOGLE_API_KEY"] = os.environ.get(
        "GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY"
    )

    # embedding_req = EmbeddingRequest(
    #     model="models/embedding-001",
    #     text="The quick brown fox jumps over the lazy dog."
    # )
    # embedding_res = get_embedding(embedding_req)
    # print(f"Embedding dimensions: {len(embedding_res.embedding['values'])}")
    # print(f"First 10 values: {embedding_res.embedding['values'][:10]}")

    # embedding_req_sentence = EmbeddingRequest(
    #     model="models/embedding-001",
    #     text="A delicious pizza was served for dinner."
    # )
    # embedding_res_sentence = get_embedding(embedding_req_sentence)
    # print(f"Embedding dimensions for sentence: {len(embedding_res_sentence.embedding['values'])}")
    pass
