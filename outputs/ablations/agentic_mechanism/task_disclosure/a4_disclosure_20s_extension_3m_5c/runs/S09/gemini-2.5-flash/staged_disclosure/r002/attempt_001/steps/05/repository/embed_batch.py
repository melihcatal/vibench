import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_batch_texts(texts: list[str]) -> list:
    """Generates embeddings for a batch of texts using Vertex AI's TextEmbeddingModel."""
    vertexai.init(project="YOUR_PROJECT_ID", location="us-central1") # Replace with your project ID and desired location
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    example_texts = [
        "This is an example text.",
        "Another text for embedding.",
        "Vertex AI provides powerful machine learning services."
    ]
    
    # NOTE: Replace "YOUR_PROJECT_ID" with your actual Google Cloud Project ID
    # and ensure Vertex AI API is enabled in your project.
    # Also, make sure you have authenticated to Google Cloud (e.g., using `gcloud auth application-default login`)
    # before running this script.

    try:
        batch_embeddings = embed_batch_texts(example_texts)
        for i, embedding in enumerate(batch_embeddings):
            print(f"Embedding for text '{example_texts[i]}': {embedding[:5]}...") # Print first 5 dimensions
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have replaced 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID,")
        print("the Vertex AI API is enabled, and you are authenticated to Google Cloud.")
