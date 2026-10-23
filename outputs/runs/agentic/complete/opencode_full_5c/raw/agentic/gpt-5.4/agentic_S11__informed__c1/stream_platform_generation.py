from __future__ import annotations

from typing import Any, Dict, List

from model_client import create_platform_client, resolve_chat_resource
from model_models import PlatformRequest, flatten_texts, stream_event_text


def stream_platform_generation(request: PlatformRequest) -> Dict[str, Any]:
    client = create_platform_client()
    deployment = resolve_chat_resource()
    events: List[Any] = []
    deltas: List[str] = []
    with client.responses.stream(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
        top_p=request.top_p,
    ) as stream:
        for event in stream:
            events.append(event)
            text = stream_event_text(event)
            if text:
                deltas.append(text)
        final_response = stream.get_final_response()
    return {
        "resource_id": deployment,
        "text": flatten_texts(deltas) or getattr(final_response, "output_text", ""),
        "events": events,
        "final_response": final_response,
    }
