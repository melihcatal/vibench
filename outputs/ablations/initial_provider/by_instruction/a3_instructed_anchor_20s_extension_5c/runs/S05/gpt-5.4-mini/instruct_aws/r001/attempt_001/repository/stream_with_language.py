from typing import AsyncIterator

from speech_client import build_transcribe_stream_client, load_streaming_speech_config
from speech_models import normalize_result_payload


async def stream_with_language(language_code: str, enable_punctuation: bool = True) -> AsyncIterator[str]:
    config = load_streaming_speech_config()
    client = build_transcribe_stream_client(config.region)
    stream = await client.start_stream_transcription(
        language_code=language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
        show_speaker_label=False,
        vocabulary_filter_method="remove",
        enable_partial_results_stabilization=True,
    )
    async for event in stream.output_stream:
        for result in event.get("Transcript", {}).get("Results", []):
            normalized = normalize_result_payload(result)
            if normalized.text:
                yield normalized.text if enable_punctuation else normalized.text.replace(".", "")
