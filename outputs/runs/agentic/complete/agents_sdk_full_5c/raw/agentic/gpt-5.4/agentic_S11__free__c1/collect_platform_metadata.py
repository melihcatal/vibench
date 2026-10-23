from __future__ import annotations

from model_client import build_generative_model, load_platform_selection
from model_models import GenerationRequest, coalesce_text, normalize_usage



def collect_platform_metadata(request: GenerationRequest) -> dict:
    selection = load_platform_selection()
    model = build_generative_model(selection)
    response = model.generate_content(
        request.to_messages(),
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    candidates = getattr(response, "candidates", []) or []
    first = candidates[0] if candidates else None
    parts = []
    if first and getattr(first, "content", None):
        parts = [getattr(part, "text", None) for part in first.content.parts]
    return {
        "output_text": coalesce_text(parts) or getattr(response, "text", ""),
        "model": selection.publisher_model,
        "resource_name": selection.model_resource,
        "usage": normalize_usage(getattr(response, "usage_metadata", None)),
        "response_id": getattr(response, "response_id", None),
        "raw_response": response,
    }
