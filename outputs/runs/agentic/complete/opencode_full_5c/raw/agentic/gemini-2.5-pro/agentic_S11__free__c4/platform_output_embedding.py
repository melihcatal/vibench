from vertexai.language_models import TextEmbeddingModel
from model_models import EmbeddingResponse
from model_client import get_google_cloud_project, get_google_cloud_location
import vertexai


def get_text_embedding(text: str) -> EmbeddingResponse:
    """
    Embeds platform outputs for evaluation or retrieval using Vertex AI Embeddings.

    Args:
        text: The text content to embed.

    Returns:
        An EmbeddingResponse containing the original text and its embedding vector.
    """
    project_id = get_google_cloud_project()
    location = get_google_cloud_location()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)

    # Use a concrete model identifier
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([text])

    vector = embeddings[0].values

    return EmbeddingResponse(text=text, embedding=vector)


if __name__ == "__main__":
    try:
        from invoke_platform_model import invoke_model

        # 1. Get text from the platform model
        model_response = invoke_model(
            "Explain the concept of machine learning in one sentence."
        )
        print(f"Original text: {model_response.text}")

        # 2. Get the embedding for the output
        embedding_response = get_text_embedding(model_response.text)
        print(
            f"Embedding vector (first 5 dimensions): {embedding_response.embedding[:5]}"
        )
        print(f"Embedding vector dimension: {len(embedding_response.embedding)}")

    except (ValueError, ImportError) as e:
        print(f"Error generating embedding: {e}")
