from google.cloud import speech

from speech_client import build_streaming_config, get_speech_client
from speech_models import normalize_transcript_event


async def stream_chunks(payload, config=None):
    config = config or {}
    client = get_speech_client()
    merged = {**payload, **config}
    streaming_config = build_streaming_config(merged)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in merged["audio_chunks"])
    for response in client.streaming_recognize(config=streaming_config, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield normalize_transcript_event(result.alternatives[0].transcript, result.is_final)
