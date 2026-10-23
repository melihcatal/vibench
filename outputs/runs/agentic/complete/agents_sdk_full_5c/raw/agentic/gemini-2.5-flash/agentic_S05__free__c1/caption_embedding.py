from google.cloud import aiplatform

def get_text_embedding(text: str, project_id: str, location: str = "us-central1", model_name: str = "text-embedding-gecko@003") -> list[float]:
    """Generates a text embedding for the given text using a Vertex AI embedding model."""
    aiplatform.init(project=project_id, location=location)

    # The EmbeddingModel is used for text embeddings.
    # Using a specific version (e.g., @003) is often recommended for stability.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(model_name)

    # Embedding input can be a list of texts; for a single text, pass it in a list.
    embeddings = model.get_embeddings([text])

    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update with your project ID

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please update YOUR_PROJECT_ID in caption_embedding.py to your Google Cloud Project ID.")
    else:
        print("Generating caption embeddings...")

        caption_1 = "The meeting minutes discussed the upcoming product launch features."
        embedding_1 = get_text_embedding(caption_1, YOUR_PROJECT_ID)
        print(f"Caption 1: '{caption_1}'\nEmbedding (first 5 values): {embedding_1[:5]}...\n")

        caption_2 = "We need to finalize the marketing campaign for the new software."
        embedding_2 = get_text_embedding(caption_2, YOUR_PROJECT_ID)
        print(f"Caption 2: '{caption_2}'\nEmbedding (first 5 values): {embedding_2[:5]}...\n")

        caption_3 = "Reviewing the quarterly financial results and future projections."
        embedding_3 = get_text_embedding(caption_3, YOUR_PROJECT_ID)
        print(f"Caption 3: '{caption_3}'\nEmbedding (first 5 values): {embedding_3[:5]}...\n")

        # You can then use these embeddings for semantic search (e.g., in a vector database)
