from model_client import get_default_model, get_google_client
from model_models import PlatformRequest, to_response


def collect_platform_metadata(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    response = client.models.generate_content(
        model=model_name,
        contents=request.prompt,
        config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    text = getattr(response, "text", None) or response.candidates[0].content.parts[0].text
    metadata = {
        "model": model_name,
        "usage": getattr(response, "usage_metadata", None),
        "response_id": getattr(response, "response_id", None),
    }
    return to_response(text, model=model_name, usage=metadata.get("usage"), metadata=metadata)
