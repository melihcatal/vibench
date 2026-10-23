import os
from typing import List
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions
from safety_models import ModerationReasonEmbeddingRequest, ModerationReasonEmbeddingResponse


def moderation_reason_embedding(payload: ModerationReasonEmbeddingRequest, config=None) -> ModerationReasonEmbeddingResponse:
    config = config or {}
    project_id = config.get('GOOGLE_CLOUD_PROJECT', os.environ.get('GOOGLE_CLOUD_PROJECT'))
    location = config.get('GOOGLE_CLOUD_LOCATION', os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1'))

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    # Initialize the Vertex AI client
    aiplatform.init(project=project_id, location=location)

    # The embedding model to use
    model_name = "text-embedding-004"
    model = aiplatform.get_model_registry().get_model(model_name)

    embeddings: List[List[float]] = []
    for reason in payload.reasons:
        response = model.predict(instances=[{'text_content': reason}])
        # Assuming the response format gives us a list of embeddings, take the first one.
        if response.predictions:
            embeddings.append(response.predictions[0]["embeddings"])

    return ModerationReasonEmbeddingResponse(embeddings=embeddings)
