import os
import boto3
from speech_client import get_speech_client


def diarized_transcription(audio_file_path, max_speakers=2):
    """Submit a batch transcription job with speaker diarization enabled.

    Parameters
    ----------
    audio_file_path : str
        Path to the audio file.
    max_speakers : int, optional
        Maximum number of distinct speakers to identify.

    Returns
    -------
    dict
        The JSON output containing speaker labels and transcript.
    """
    client = get_speech_client("boto3")
    job_name = (
        f"diarized-{os.path.basename(audio_file_path).split(',')[0]}-{int(time.time())}"
    )
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={
            "MediaFileUri": f"s3://{os.getenv('AWS_S3_BUCKET__STT__INPUTS')}/{os.path.basename(audio_file_path)}"
        },
        MediaFormat="wav",
        LanguageCode="en-US",
        Settings={
            "EnableSpeakerIdentification": True,
            "MaxSpeakerLabels": max_speakers,
        },
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]
