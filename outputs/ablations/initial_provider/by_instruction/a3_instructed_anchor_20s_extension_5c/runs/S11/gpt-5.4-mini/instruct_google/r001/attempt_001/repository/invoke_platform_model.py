from model_client import get_client, get_model_name
from model_models import ModelRequest, ModelResponse, extract_metadata, normalize_text


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    client = get_client()
    model_name = request.model or get_model_name()
    response = client.models.generate_content(
        model=model_name,
        contents=request.prompt,
        config={"temperature": request.temperature} if request.temperature is not None else None,
    )
    return ModelResponse(text=normalize_text(response), metadata=extract_metadata(response))
