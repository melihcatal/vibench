import assemblyai as aai
from speech_client import get_client, poll_for_completion
from speech_models import extract_diarized_transcript

def diarized_transcript(audio_url: str) -> list:
    """
    Requests speaker diarization for a recorded meeting.
    Submits job with diarization, polls, returns list of speaker segments.
    """
    client = get_client()
    config = aai.TranscriptionConfig(
        audio_url=audio_url,
        speaker_labels=True
    )
    transcript = client.transcripts.create(config)
    polled_transcript = poll_for_completion(client, transcript.id)
    return extract_diarized_transcript(polled_transcript)