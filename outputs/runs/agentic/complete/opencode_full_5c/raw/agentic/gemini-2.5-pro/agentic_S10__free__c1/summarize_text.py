from model_client import get_model_client
from model_models import SummarizeRequest, SummarizeResponse


def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    cohere_client = get_model_client()
    response = cohere_client.summarize(
        text=request.text,
        length=request.length,
        format=request.format,
        model=request.model,
        extractiveness=request.extractiveness,
        temperature=request.temperature,
    )
    return SummarizeResponse(summary=response.summary, meta=response.meta)
