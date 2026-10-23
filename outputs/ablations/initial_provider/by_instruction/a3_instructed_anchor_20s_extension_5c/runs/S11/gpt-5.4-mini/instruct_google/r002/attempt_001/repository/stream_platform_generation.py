from model_client import get_default_model, get_google_client
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    stream = client.models.generate_content_stream(
        model=model_name,
        contents=request.prompt,
        config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return stream
