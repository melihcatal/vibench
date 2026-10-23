import os
from model_client import get_vertex_ai_model
from model_models import ModelResponse
import vertexai


def collect_platform_metadata(prompt: str) -> ModelResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Example location
    model_name = "text-bison@002"  # Specific Vertex AI model

    vertexai.init(project=project_id, location=location)
    model = vertexai.preview.language_models.TextGenerationModel.from_pretrained(
        model_name
    )

    response = model.predict(prompt=prompt)

    # Vertex AI response objects directly contain metadata like safety_attributes
    # Usage information might require inspecting the client library or API response in more detail
    metadata = {
        "safety_attributes": response.safety_attributes.to_dict()
        if response.safety_attributes
        else None,
        "model_name": model_name,
        "_raw_response_object_fields": [
            field.name for field in response._pb.ListFields()
        ],
    }

    return ModelResponse(text=response.text, metadata=metadata)
