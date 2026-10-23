import boto3
from speech_client import SpeechClient

client = SpeechClient()  # boto3 helper


def get_timestamped_transcript(job_id):
    """
    Retrieves the completed transcription job result and extracts word-level timestamps.
    Returns a list of dicts: [{"start": float, "end": float, "text": str}, ...]
    """
    response = client.transcribe.get_transcription_job(TranscriptionJobName=job_id)
    result = response["TranscriptionJob"]["Transcript"]["Transcript"]
    # Amazon Transcribe returns a delimited string; parse it into structured timestamps
    timestamps = []
    for seg in result.splitlines():
        start, duration, text = seg.split(" ")[:3]
        timestamps.append(
            {"start": float(start), "duration": float(duration), "text": text}
        )
    return timestamps
