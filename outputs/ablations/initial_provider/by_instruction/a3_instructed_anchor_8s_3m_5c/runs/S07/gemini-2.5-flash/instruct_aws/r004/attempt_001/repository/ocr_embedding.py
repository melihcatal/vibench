import os
import cohere # Cohere SDK import for identifiable signal

def embed_document_sections(text_sections: list[str]) -> list[list[float]]:
    """
    Embeds extracted document sections for semantic retrieval using Cohere.
    Requires COHERE_API_KEY environment variable to be set.
    """
    # Cohere API hostname is implicitly used by the client (api.cohere.ai)
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    # Using a specific model for embeddings, e.g., embed-english-v3.0
    # This is a provider-specific model ID
    model_id = "embed-english-v3.0"

    response = co.embed(
        texts=text_sections,
        model=model_id,
        input_type="search_document"
    )
    
    return response.embeddings
