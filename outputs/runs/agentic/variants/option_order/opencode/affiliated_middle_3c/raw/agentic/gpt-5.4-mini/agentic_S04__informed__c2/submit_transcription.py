from speech_client import create_transcriber, resolve_audio_source
from speech_models import TranscriptionRequest, normalize_assemblyai_transcript


def submit_transcription(request: TranscriptionRequest):
    transcriber = create_transcriber()
    source = resolve_audio_source(request.audio_url, request.audio_file)
    config = {
        "speaker_labels": request.speaker_labels,
        "auto_highlights": False,
        "punctuate": True,
    }
    if request.language_code:
        config["language_code"] = request.language_code
    transcript = transcriber.transcribe(source, config=config)
    return normalize_assemblyai_transcript(transcript.__dict__)
