from speech_client import get_speech_client
from speech_models import TranscriptionJob


def request_diarization(audio_url: str) -> TranscriptionJob:
    """
    Submits a job to AssemblyAI with speaker diarization enabled.
    """
    client = get_speech_client()
    config = {"audio_url": audio_url, "speaker_labels": True}
    transcript = client.transcripts.submit(config)
    return TranscriptionJob(id=transcript.id, status=transcript.status)


def get_diarized_transcript(job_id: str) -> list:
    """
    Retrieves a completed transcript and returns diarized utterances.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(transcript_id=job_id)

    if transcript.status != "completed":
        return []

    utterances = []
    if transcript.utterances:
        for utterance in transcript.utterances:
            utterances.append({"speaker": utterance.speaker, "text": utterance.text})

    return utterances
