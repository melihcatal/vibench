from speech_client import get_speech_client, upload_audio

def request_diarized_transcript(audio_file_path: str) -> str:
    """
    Request speaker diarization for a recorded meeting.
    Submit audio file with speaker labels enabled.
    Returns the job ID.
    """
    client = get_speech_client()
    audio_url = upload_audio(client, audio_file_path)
    transcript = client.transcripts.create(
        audio_url=audio_url,
        speaker_labels=True
    )
    return transcript.id
