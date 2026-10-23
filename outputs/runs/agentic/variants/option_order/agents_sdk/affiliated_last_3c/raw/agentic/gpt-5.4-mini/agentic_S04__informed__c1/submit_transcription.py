from speech_client import SpeechClientFactory, build_audio_url, make_job_request


def submit_transcription(audio_file: str, speaker_labels: bool = False) -> str:
    transcriber = SpeechClientFactory.transcription_api()
    request = make_job_request(build_audio_url(audio_file), speaker_labels=speaker_labels)
    result = transcriber.transcribe(request.audio_url, speaker_labels=request.speaker_labels)
    return getattr(result, "id", "") or getattr(result, "audio_url", "")
