from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from document_models import EmbeddingRequest, EmbeddingResponse

# Initialize Vertex AI SDK (adjust project/location as needed)
aiplatform.init(project="your-gcp-project-id", location="us-central1")

def embed_ocr_sections(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI (text-embedding-gecko)."""
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@001") # Using a specific stable model version

    # The Vertex AI embedding model can take a list of texts.
    embeddings_response = model.get_embeddings(request.text_segments)

    # Extract the numerical embeddings from the response objects.
    extracted_embeddings = [embedding.values for embedding in embeddings_response]

    return EmbeddingResponse(embeddings=extracted_embeddings)
