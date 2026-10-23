from __future__ import annotations

from typing import Optional

from model_client import get_generative_model
from model_models import GenerationRequest, GenerationResult, candidate_text, usage_to_dict
from select_platform_resource import select_platform_resource


def invoke_platform_model(
    prompt: str,
    task_profile: str = "balanced",
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> GenerationResult:
    selection = select_platform_resource(task_profile=task_profile, project_id=project_id, location=location)
    model = get_generative_model(selection)
    request = GenerationRequest(prompt=prompt)
    response = model.generate_content(
        request.to_messages(),
        generation_config={
            "max_output_tokens": request.max_tokens,
            "temperature": request.temperature,
        },
    )
    return GenerationResult(
        text=candidate_text(response),
        model=selection.model_name,
        usage=usage_to_dict(getattr(response, "usage_metadata", None)),
        resource={
            "publisher_model": selection.publisher_model,
            "location": selection.location,
            "project_id": selection.project_id,
        },
        raw=response,
    )
