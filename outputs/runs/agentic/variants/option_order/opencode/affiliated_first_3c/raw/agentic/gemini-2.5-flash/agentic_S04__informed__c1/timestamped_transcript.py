import requests
from speech_client import SpeechClient
from speech_models import TranscriptionResult


def get_timestamped_transcript(job_name: str) -> TranscriptionResult:
    client = SpeechClient().get_client()

    response = client.get_transcription_job(TranscriptionJobName=job_name)
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    if status == "COMPLETED":
        transcript_file_uri = response["TranscriptionJob"]["Transcript"][
            "TranscriptFileUri"
        ]
        transcript_content = requests.get(transcript_file_uri).json()

        timestamped_segments = []
        for item in transcript_content["results"]["items"]:
            if "start_time" in item and "end_time" in item:
                timestamped_segments.append(
                    {
                        "word": item["alternatives"][0]["content"],
                        "start_time": float(item["start_time"]),
                        "end_time": float(item["end_time"]),
                    }
                )

        return TranscriptionResult(
            job_name=job_name, status=status, timestamped_segments=timestamped_segments
        )
    else:
        return TranscriptionResult(
            job_name=job_name, status=status, timestamped_segments=None
        )
