from google.cloud import aiplatform

from speech_models import normalize_transcript


def embed_caption_chunk(text: str) -> list[float]:
    endpoint = aiplatform.Endpoint(endpoint_name="projects/PROJECT/locations/us-central1/endpoints/EMBEDDING_ENDPOINT")
    instance = normalize_transcript(text)
    prediction = endpoint.predict(instances=[{"content": instance}])
    return prediction.predictions[0]["embeddings"] if prediction.predictions else []
