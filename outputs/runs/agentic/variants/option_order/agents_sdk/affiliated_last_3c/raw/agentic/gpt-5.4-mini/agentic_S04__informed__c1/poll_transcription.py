from speech_client import SpeechClientFactory, normalize_transcript


def poll_transcription(job_id: str):
    transcriber = SpeechClientFactory.transcription_api()
    result = transcriber.get_transcript(job_id)
    return normalize_transcript(result)
