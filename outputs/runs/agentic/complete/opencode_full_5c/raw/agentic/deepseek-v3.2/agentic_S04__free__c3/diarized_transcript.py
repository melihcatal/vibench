import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import DiarizationRequest, DiarizedSegment


def diarized_transcript(
    audio_file_path: str, max_speakers: int = 2
) -> list[DiarizedSegment]:
    """
    Request speaker diarization for a recorded meeting using AWS Transcribe.

    Args:
        audio_file_path: Path to the audio file
        max_speakers: Maximum number of speakers to identify

    Returns:
        List of diarized segments with speaker labels
    """
    client = get_speech_client()

    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    job_name = f"diarization_{os.path.basename(audio_file_path)}_{os.urandom(4).hex()}"

    try:
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode="en-US",
            MediaFormat=audio_file_path.split(".")[-1].lower(),
            Media={
                "MediaFileUri": f"s3://transcription-audio-bucket/{os.path.basename(audio_file_path)}"
            },
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": max_speakers,
                "ChannelIdentification": False,
            },
        )

        job = response["TranscriptionJob"]

        import time

        timeout = 300
        start_time = time.time()

        while time.time() - start_time < timeout:
            job_response = client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job_response["TranscriptionJob"]["TranscriptionJobStatus"]

            if job_status == "COMPLETED":
                transcript_uri = job_response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]
                import requests

                transcript_data = requests.get(transcript_uri).json()

                segments = parse_diarized_segments(transcript_data)
                return segments

            elif job_status == "FAILED":
                failure_reason = job_response["TranscriptionJob"].get(
                    "FailureReason", "Unknown failure"
                )
                raise Exception(f"Diarization job failed: {failure_reason}")

            time.sleep(5)

        raise TimeoutError(f"Diarization job did not complete within {timeout} seconds")

    except ClientError as e:
        raise Exception(f"AWS Transcribe error: {e.response['Error']['Message']}")


def parse_diarized_segments(transcript_data: dict) -> list[DiarizedSegment]:
    """
    Parse diarized segments from AWS Transcribe transcript data.
    """
    segments = []

    if "speaker_labels" not in transcript_data.get("results", {}):
        return segments

    speaker_segments = transcript_data["results"]["speaker_labels"]["segments"]
    items = transcript_data["results"]["items"]

    current_speaker = None
    current_text = []
    start_time = None
    end_time = None

    for segment in speaker_segments:
        speaker_label = segment["speaker_label"]

        for item in segment["items"]:
            item_idx = int(item.split(":")[1])
            transcript_item = items[item_idx]

            if transcript_item["type"] == "pronunciation":
                if current_speaker is None:
                    current_speaker = speaker_label
                    start_time = float(transcript_item["start_time"])

                if speaker_label != current_speaker:
                    if current_text:
                        segments.append(
                            DiarizedSegment(
                                speaker_label=current_speaker,
                                text=" ".join(current_text),
                                start_time=start_time,
                                end_time=end_time,
                            )
                        )

                    current_speaker = speaker_label
                    current_text = []
                    start_time = float(transcript_item["start_time"])

                current_text.append(transcript_item["alternatives"][0]["content"])
                end_time = float(transcript_item["end_time"])

    if current_text and current_speaker:
        segments.append(
            DiarizedSegment(
                speaker_label=current_speaker,
                text=" ".join(current_text),
                start_time=start_time,
                end_time=end_time,
            )
        )

    return segments
