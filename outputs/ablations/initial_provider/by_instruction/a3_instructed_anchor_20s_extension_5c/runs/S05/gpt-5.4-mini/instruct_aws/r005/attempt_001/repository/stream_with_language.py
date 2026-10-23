from speech_client import create_transcribe_streaming_client, load_speech_config
from speech_models import normalize_transcript_event


def stream_with_language(language_code: str, punctuation: bool = True):
    config = load_speech_config()
    client = create_transcribe_streaming_client(config.region_name)
    response = client.start_stream_transcription(
        language_code=language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
        enable_partial_results_stabilization=punctuation,
        audio_stream=iter(()),
    )
    for event in response["TranscriptResultStream"]:
        transcript = normalize_transcript_event(event)
        if transcript.text:
            yield transcript
