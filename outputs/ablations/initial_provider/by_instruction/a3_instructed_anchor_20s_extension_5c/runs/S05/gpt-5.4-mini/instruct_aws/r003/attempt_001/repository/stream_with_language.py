from typing import Iterator, Optional

from speech_client import load_speech_config, make_transcribe_streaming_client
from speech_models import TranscriptChunk


def stream_with_language(language_code: Optional[str] = None, punctuation: Optional[bool] = None) -> Iterator[TranscriptChunk]:
    config = load_speech_config(language_code=language_code, punctuation=punctuation)
    client = make_transcribe_streaming_client(config.region_name)
    response = client.start_stream_transcription(
        LanguageCode=config.language_code,
        MediaSampleRateHertz=config.media_sample_rate_hz,
        MediaEncoding=config.media_encoding,
        EnablePartialResultsStabilization=True,
        ShowSpeakerLabel=False,
        EnableAutomaticPunctuation=config.punctuation,
        AudioStream=iter(()),
    )
    for event in response["TranscriptResultStream"]:
        for result in event.get("TranscriptEvent", {}).get("Transcript", {}).get("Results", []):
            alternatives = result.get("Alternatives", [])
            if alternatives:
                yield TranscriptChunk(text=alternatives[0].get("Transcript", ""), is_partial=result.get("IsPartial", False), language_code=config.language_code)
