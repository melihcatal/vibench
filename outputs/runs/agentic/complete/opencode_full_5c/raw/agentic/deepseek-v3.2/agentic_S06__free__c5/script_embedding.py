from google.cloud import aiplatform
import numpy as np


def embed_narration_script(text, model_id="textembedding-gecko@001"):
    """Embed narration scripts for voice-asset search using Google Vertex AI."""
    aiplatform.init(project="your-project-id", location="us-central1")

    from google.cloud.aiplatform_v1beta1.types import content as content_types
    from google.cloud import aiplatform_v1beta1

    client = aiplatform_v1beta1.PredictionServiceClient()

    endpoint = f"projects/your-project-id/locations/us-central1/publishers/google/models/{model_id}"

    instance = content_types.Content(parts=[content_types.Part(text=text)])

    request = aiplatform_v1beta1.PredictRequest(endpoint=endpoint, instances=[instance])

    response = client.predict(request=request)

    if response.predictions and len(response.predictions) > 0:
        embedding = response.predictions[0].get("embeddings", {}).get("values", [])
        if embedding:
            return np.array(embedding)

    return None


def search_similar_voices(query_embedding, voice_embeddings_db, top_k=5):
    """Search for similar voices using embedding similarity."""
    if query_embedding is None or not voice_embeddings_db:
        return []

    similarities = []
    for voice_id, voice_embedding in voice_embeddings_db.items():
        if voice_embedding is not None:
            similarity = np.dot(query_embedding, voice_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(voice_embedding)
            )
            similarities.append((voice_id, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]
