from google.cloud import aiplatform
from model_models import ModelConfig, EmbeddingOutput
from typing import List

def embed_platform_output(
    text: str, config: ModelConfig
) -> EmbeddingOutput:
    # Initialize Vertex AI client for embeddings
    aiplatform.init(project=config.project_id, location=config.location)

    # Use a specific embedding model from Vertex AI
    # For example, 'text-embedding-004' or a universal sentence encoder model
    # The model_id in config should be an embedding model ID here.
    # We'll assume the config.model_id is set to an embedding model like 'text-embedding-004'
    embedding_model_id = config.model_id # Expected to be an embedding model ID

    # The Vertex AI TextGenerationModel can also perform embeddings.
    # Using TextGenerationModel for embedding as it's a common way to access embedding from Vertex AI.
    model = aiplatform.TextGenerationModel.from_pretrained(embedding_model_id)

    # Embed the text
    # The method for embedding is typically `get_embeddings` on an embedding model client
    # or a specific method if using TextGenerationModel for this purpose.
    # For clarity, let's use the dedicated `TextEmbeddingModel.from_pretrained` and `get_embeddings`
    embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(embedding_model_id)
    
    embeddings_response = embedding_model.get_embeddings([text])

    embedding_vector: List[float] = []
    if embeddings_response.embeddings:
        embedding_vector = embeddings_response.embeddings[0].values

    return EmbeddingOutput(
        embedding=embedding_vector,
        model_id=embedding_model_id
    )
