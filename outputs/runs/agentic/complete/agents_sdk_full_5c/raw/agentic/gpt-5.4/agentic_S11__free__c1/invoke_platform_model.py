from __future__ import annotations

from model_client import build_generative_model, load_platform_selection
from model_models import GenerationRequest, GenerationResult, coalesce_text, normalize_usage



def invoke_platform_model(request: GenerationRequest) -> GenerationResult:
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
        for part in first.content.parts:
            parts.append(getattr(part, "text", None))
    text = coalesce_text(parts) or getattr(response, "text", "")
    return GenerationResult(
        text=text,
        model=selection.publisher_model,
        usage=normalize_usage(getattr(response, "usage_metadata", None)),
        resource=selection.model_resource,
        raw=response,
    )
