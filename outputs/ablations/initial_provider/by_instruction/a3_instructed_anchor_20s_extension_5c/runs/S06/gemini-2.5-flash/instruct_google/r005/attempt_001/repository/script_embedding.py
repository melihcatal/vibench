from google.cloud import aiplatform
from typing import List

def embed_script(text: str) -> List[float]:
    """Embeds narration scripts for voice-asset search using Google Cloud Vertex AI Text Embedding API.

    The model used is `textembedding-gecko`.
    """
    # Initialize Vertex AI
    # aiplatform.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")
    # Replace 'YOUR_PROJECT_ID' and 'YOUR_REGION' with actual values or use environment variables.
    # For this example, we assume project and location are configured or will be provided via env vars.

    # The TextEmbeddingModel can be initialized with a specific model_name.
    # The default is "textembedding-gecko".
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings = model.get_embeddings([text])

    # The get_embeddings method returns a list of objects, each containing an embedding vector.
    # We are processing a single text, so we take the first (and only) embedding.
    return embeddings[0].values
