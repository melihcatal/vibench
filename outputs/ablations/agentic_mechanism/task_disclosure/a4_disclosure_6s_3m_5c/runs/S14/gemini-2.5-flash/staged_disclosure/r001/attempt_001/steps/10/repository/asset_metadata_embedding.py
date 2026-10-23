import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_asset_data(metadata: dict, extracted_text: str) -> list:
    """
    Embeds object metadata and extracted text using Vertex AI's TextEmbeddingModel.

    Args:
        metadata (dict): A dictionary of object metadata (e.g., {"title": "document A", "author": "John Doe"}).
        extracted_text (str): The extracted text content of the object.

    Returns:
        list: A list of embedding vectors.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Combine metadata values into a single string for embedding
    metadata_string = " ".join(f"{k}: {v}" for k, v in metadata.items())
    
    # Combine metadata string and extracted text
    combined_text = f"{metadata_string} {extracted_text}"

    embeddings = model.get_embeddings([combined_text])
    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    sample_metadata = {"title": "Annual Report 2023", "department": "Finance"}
    sample_text = "This report summarizes the financial performance for the year 2023..."
    
    # Example usage:
    # Make sure to replace "your-gcp-project-id" with your actual GCP project ID
    # and authenticate with GCP (e.g., `gcloud auth application-default login`)
    try:
        asset_embeddings = embed_asset_data(sample_metadata, sample_text)
        print("Generated embedding vector (first 5 dimensions):")
        print(asset_embeddings[0][:5])
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have replaced 'your-gcp-project-id' with your actual GCP project ID and authenticated with GCP.")
        print("You can authenticate by running: gcloud auth application-default login")
