from google.cloud import aiplatform
from storage_models import AssetMetadataEmbeddingRequest

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest):
    aiplatform.init(project="YOUR_GCP_PROJECT_ID", location="us-central1") # Replace YOUR_GCP_PROJECT_ID with actual project ID

    # Using the TextEmbeddingModel for embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")

    # Combine metadata and extracted text for embedding
    text_to_embed = f"Object Name: {request.object_name}. "
    if request.extracted_text:
        text_to_embed += f"Extracted Text: {request.extracted_text}"

    embeddings = model.get_embeddings([text_to_embed])
    
    # The embeddings object contains a list of Embedding objects, each with a values attribute.
    # We extract the first embedding's values.
    embedding_values = embeddings[0].values

    return {
        "object_name": request.object_name,
        "embedding": embedding_values,
        "model_id": "textembedding-gecko"
    }
