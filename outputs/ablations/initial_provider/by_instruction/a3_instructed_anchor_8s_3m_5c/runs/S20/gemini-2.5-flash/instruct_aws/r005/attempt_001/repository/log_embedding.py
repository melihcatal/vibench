import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')

    aiplatform.init(project=project_id, location=location)

    # Use the TextEmbeddingModel for embeddings
    # The model ID for text embeddings can vary. "textembedding-gecko@001" is a common one.
    model_id = os.environ.get('GOOGLE_CLOUD_EMBEDDING_MODEL_ID', 'textembedding-gecko@003')

    from vertexai.language_models import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained(model_id)
    embeddings_results = []

    try:
        # The `model.get_embeddings` method can take a list of texts
        response = model.get_embeddings(log_messages)

        for i, embedding in enumerate(response):
            embeddings_results.append({
                'original_text': log_messages[i],
                'embedding': embedding.values
            })

    except Exception as e:
        # Handle errors during embedding generation
        for message in log_messages:
            embeddings_results.append({
                'original_text': message,
                'error': str(e)
            })

    return embeddings_results
