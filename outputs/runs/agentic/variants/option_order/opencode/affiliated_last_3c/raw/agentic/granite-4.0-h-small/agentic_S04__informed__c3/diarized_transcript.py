import boto3
from speech_client import SpeechClient

client = SpeechClient()  # boto3 helper


def request_diarized_transcription(audio_file_path, job_name, max_speakers=2):
    """Requests speaker diarization for a meeting recording using Amazon Transcribe.
    Returns the transcription job name.
    """
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    payload = client.create_diarized_transcription_payload(
        audio_file_path, job_name, max_speakers
    )
    client.transcribe.start_transcription_job(**payload)
    return payload["TranscriptionJobName"]
