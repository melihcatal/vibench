
from google.cloud import aiplatform

def embed_for_search(query: str, documents: list[str], project_id: str, location: str):
    """
    Embeds a query and documents using Google Cloud Vertex AI's textembedding-gecko model.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.
        project_id: Your Google Cloud project ID.
        location: The GCP region where the Vertex AI endpoint is available (e.g., "us-central1").

    Returns:
        A tuple containing the query embedding and a list of document embeddings.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("textembedding-gecko")

    query_embedding = model.predict([query]).embeddings[0].values
    document_embeddings = [embedding.values for embedding in model.predict(documents).embeddings]

    return query_embedding, document_embeddings

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and location)
    PROJECT_ID = "your-gcp-project-id"  # e.g., "my-gcp-project"
    LOCATION = "us-central1"

    search_query = "What is the capital of France?"
    search_documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
        "Berlin is the capital of Germany.",
    ]

    try:
        query_vec, doc_vecs = embed_for_search(search_query, search_documents, PROJECT_ID, LOCATION)
        print("Query Embedding:", query_vec[:5], "...")  # Print first 5 dimensions for brevity
        print("Document Embeddings:")
        for i, vec in enumerate(doc_vecs):
            print(f"  Document {i+1}:", vec[:5], "...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated to GCP and enabled the Vertex AI API.")
        print("Also, replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
