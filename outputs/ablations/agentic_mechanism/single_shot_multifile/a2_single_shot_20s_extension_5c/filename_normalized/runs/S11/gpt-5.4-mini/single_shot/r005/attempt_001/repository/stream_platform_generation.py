from typing import Iterator, Optional
from model_client import get_platform_client, get_platform_model_id
from model_models import PlatformStreamEvent, PlatformStreamResult


def stream_platform_generation(prompt: str, system_instruction: Optional[str] = None) -> Iterator[PlatformStreamEvent]:
    client = get_platform_client()
    model_id = get_platform_model_id()
    stream = client.responses.stream(model=model_id, input={"input": prompt, "instructions": system_instruction} if system_instruction else prompt)
    for event in stream:
        yield PlatformStreamEvent(provider_event=event)


def collect_stream_result(prompt: str, system_instruction: Optional[str] = None) -> PlatformStreamResult:
    events = list(stream_platform_generation(prompt, system_instruction=system_instruction))
    return PlatformStreamResult(events=events)
