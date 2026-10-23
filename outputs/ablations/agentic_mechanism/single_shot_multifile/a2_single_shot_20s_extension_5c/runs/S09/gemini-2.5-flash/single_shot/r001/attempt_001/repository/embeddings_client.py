import os
from openai import OpenAI, AzureOpenAI
import cohere
import vertexai
from vertexai.language_models import TextEmbeddingModel

# --- OpenAI Client --- #
def get_openai_client() -> OpenAI:
    """Initializes and returns an OpenAI client."""
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- Azure OpenAI Client --- #
def get_azure_openai_client() -> AzureOpenAI:
    """Initializes and returns an Azure OpenAI client."""
    return AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01" # Specify your API version
    )

# --- Cohere Client --- #
def get_cohere_client() -> cohere.Client:
    """Initializes and returns a Cohere client."""
    return cohere.Client(os.environ.get("COHERE_API_KEY"))

# --- Google Vertex AI Client (for Embeddings) --- #
def get_vertexai_embedding_model() -> TextEmbeddingModel:
    """
    Initializes and returns a Google Vertex AI TextEmbeddingModel.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set or gcloud auth is configured.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set for Vertex AI.")
    
    vertexai.init(project=project_id, location=location)
    return TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
