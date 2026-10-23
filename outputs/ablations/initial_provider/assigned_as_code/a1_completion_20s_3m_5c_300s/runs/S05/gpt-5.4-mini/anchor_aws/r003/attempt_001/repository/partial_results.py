from speech_client import load_streaming_speech_config
from speech_models import TranscriptEvent, normalize_text


def parse_partial_results(event):
    transcript = getattr(getattr(event, "transcript", None), "results", None) or []
    for result in transcript:
        alternatives = getattr(result, "alternatives", None) or []
        if alternatives:
            yield TranscriptEvent(text=normalize_text(alternatives[0].transcript), is_final=not result.is_partial)


async def partial_results(payload, config=None):
    load_streaming_speech_config(payload, config)
    async for event in payload["event_stream"]:
        for item in parse_partial_results(event):
            yield {"text": item.text, "is_final": item.is_final}
