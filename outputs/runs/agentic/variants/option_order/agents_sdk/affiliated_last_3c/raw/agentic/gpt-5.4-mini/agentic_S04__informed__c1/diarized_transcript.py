from speech_client import SpeechClientFactory, make_job_request, normalize_transcript


def diarized_transcript(audio_file: str):
    transcriber = SpeechClientFactory.transcription_api()
    request = make_job_request(audio_file, speaker_labels=True)
    result = transcriber.transcribe(request.audio_url, speaker_labels=True)
    return normalize_transcript(result)
