from document_client import get_openai_client
from document_models import TextExtractionResult, EmbeddingResult


def create_text_embedding(text_to_embed: TextExtractionResult) -> EmbeddingResult:
    client = get_openai_client()

    # OpenAI embedding model identifier
    model_id = "text-embedding-ada-002"

    try:
        response = client.embeddings.create(
            input=text_to_embed.text_content, model=model_id
        )
        if response.data and len(response.data) > 0:
            embedding_vector = response.data[0].embedding
            return EmbeddingResult(
                embedding=embedding_vector, text=text_to_embed.text_content
            )
        else:
            raise Exception("No embedding data received from OpenAI.")

    except Exception as e:
        raise Exception(f"Failed to create embedding with OpenAI: {e}")
