from __future__ import annotations

from typing import Any, Dict, List

from model_client import get_openai_client
from model_models import PlatformRequest, normalize_stream_text
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Dict[str, Any]:
    resource = select_platform_resource()
    client = get_openai_client()
    events: List[Any] = []
    with client.responses.stream(
        model=resource["selected_model"],
        input=request.prompt,
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
    ) as stream:
        for event in stream:
            events.append(event)
        final_response = stream.get_final_response()
    return {
        "provider": "openai",
        "model": resource["selected_model"],
        "events": events,
        "final_response": final_response,
        "text": normalize_stream_text(events),
    }
