import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from model_client import get_vertex_ai_project_location
from model_models import PlatformEmbeddingRequest, PlatformEmbeddingResponse


def embed_platform_output(
    request: PlatformEmbeddingRequest,
) -> PlatformEmbeddingResponse:
    project, location = get_vertex_ai_project_location()
    vertexai.init(project=project, location=location)

    # Using the "text-embedding-004" model for embeddings
    model = TextEmbeddingModel.from_pretrained(request.model_id)

    embeddings = model.get_embeddings(
        [TextEmbeddingInput(request.text, task_type="RETRIEVAL_DOCUMENT")]
    )

    return PlatformEmbeddingResponse(
        embedding=embeddings[0].values,
        model_id=request.model_id,
        provider="Google Cloud Vertex AI",
    )
