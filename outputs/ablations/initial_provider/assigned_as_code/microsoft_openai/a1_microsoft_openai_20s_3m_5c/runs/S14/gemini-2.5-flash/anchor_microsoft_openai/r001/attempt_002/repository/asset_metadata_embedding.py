from vertexai.preview.language_models import TextEmbeddingModel
import os

def asset_metadata_embedding(payload):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # e.g., 'us-central1'

    if not all([project_id, location]):
        raise ValueError("Google Cloud Project ID or Location not found in environment variables.")

    text_to_embed = payload['text_to_embed'] # This can be metadata, extracted text, or a combination

    # Initialize Vertex AI for embeddings
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001") # Using textembedding-gecko@001

    embeddings = model.get_embeddings([text_to_embed])

    # The embeddings are typically a list of float values
    return {'embedding': embeddings[0].values, 'original_text': text_to_embed}
