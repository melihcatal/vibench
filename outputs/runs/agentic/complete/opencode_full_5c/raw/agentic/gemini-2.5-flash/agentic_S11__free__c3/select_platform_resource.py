import vertexai
from vertexai.language_models import TextGenerationModel
from model_client import get_vertex_ai_project_location
from model_models import ResourceSelectionRequest, ResourceSelectionResponse


def select_platform_resource(
    request: ResourceSelectionRequest,
) -> ResourceSelectionResponse:
    project, location = get_vertex_ai_project_location()
    vertexai.init(project=project, location=location)

    # In Vertex AI, selecting a "resource" often means initializing the model client
    # with a specific model ID. We'll simulate checking if the model exists/is valid.
    try:
        # Attempt to load the model to verify its existence
        model = TextGenerationModel.from_pretrained(request.model_id)
        # This is a simplified check; a real scenario might involve listing endpoints
        # or deployed models if `model_id` refers to a specific deployment.

        return ResourceSelectionResponse(
            resource_id=request.model_id,
            resource_type="model",
            status="available",
            provider="Google Cloud Vertex AI",
        )
    except Exception as e:
        return ResourceSelectionResponse(
            resource_id=request.model_id,
            resource_type="model",
            status=f"error: {str(e)}",
            provider="Google Cloud Vertex AI",
        )
