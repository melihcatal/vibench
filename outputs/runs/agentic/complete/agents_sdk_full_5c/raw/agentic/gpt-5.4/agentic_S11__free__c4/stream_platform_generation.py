from __future__ import annotations

from typing import Iterator, Optional

from model_client import get_generative_model
from model_models import GenerationRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(
    prompt: str,
    task_profile: str = "balanced",
    project_id: Optional[str] = None,
    location: Optional[str] = None,
):
    selection = select_platform_resource(task_profile=task_profile, project_id=project_id, location=location)
    model = get_generative_model(selection)
    request = GenerationRequest(prompt=prompt)
    return model.generate_content(
        request.to_messages(),
        generation_config={
            "max_output_tokens": request.max_tokens,
            "temperature": request.temperature,
        },
        stream=True,
    )


def iter_stream_text(
    prompt: str,
    task_profile: str = "balanced",
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> Iterator[tuple[object, str]]:
    for chunk in stream_platform_generation(
        prompt=prompt,
        task_profile=task_profile,
        project_id=project_id,
        location=location,
    ):
        yield chunk, getattr(chunk, "text", "")
