import os
import numpy as np
from google.cloud import aiplatform


def embed_text(text, model_id="textembedding-gecko@001"):
    """Embed narration scripts for voice-asset search using Google Vertex AI."""
    aiplatform.init(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
    )

    from google.cloud.aiplatform_v1beta1.types import content as gapic_content_types
    from google.cloud import aiplatform_v1beta1

    client = aiplatform_v1beta1.PredictionServiceClient()

    endpoint = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT')}/locations/{os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')}/publishers/google/models/{model_id}"

    instance = gapic_content_types.Content(parts=[gapic_content_types.Part(text=text)])

    request = aiplatform_v1beta1.PredictRequest(
        endpoint=endpoint, instances=[instance.to_dict()]
    )

    response = client.predict(request=request)

    if response.predictions and len(response.predictions) > 0:
        embedding = response.predictions[0].get("embeddings", {}).get("values", [])
        return np.array(embedding, dtype=np.float32)

    raise ValueError("Failed to get embedding from model")


def embed_batch(texts, model_id="textembedding-gecko@001"):
    """Embed multiple texts in a batch."""
    aiplatform.init(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
    )

    from google.cloud.aiplatform_v1beta1.types import content as gapic_content_types
    from google.cloud import aiplatform_v1beta1

    client = aiplatform_v1beta1.PredictionServiceClient()

    endpoint = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT')}/locations/{os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')}/publishers/google/models/{model_id}"

    instances = []
    for text in texts:
        instance = gapic_content_types.Content(
            parts=[gapic_content_types.Part(text=text)]
        )
        instances.append(instance.to_dict())

    request = aiplatform_v1beta1.PredictRequest(endpoint=endpoint, instances=instances)

    response = client.predict(request=request)

    embeddings = []
    for prediction in response.predictions:
        embedding = prediction.get("embeddings", {}).get("values", [])
        embeddings.append(np.array(embedding, dtype=np.float32))

    return embeddings


def cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings."""
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
