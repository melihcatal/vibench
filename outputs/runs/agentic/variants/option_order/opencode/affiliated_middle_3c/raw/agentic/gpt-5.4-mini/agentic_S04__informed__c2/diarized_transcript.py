from speech_client import create_transcriber, resolve_audio_source
from speech_models import TranscriptionRequest, extract_diarized_speakers


def diarized_transcript(request: TranscriptionRequest):
    transcriber = create_transcriber()
    source = resolve_audio_source(request.audio_url, request.audio_file)
    config = {"speaker_labels": True, "punctuate": True}
    transcript = transcriber.transcribe(source, config=config)
    payload = transcript.__dict__
    return {
        "text": payload.get("text", ""),
        "speakers": extract_diarized_speakers(payload),
        "raw": payload,
    }
