import os
import json
import urllib.request
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, LanguageCode, SpeakerSegment


def request_diarized_transcription(
    audio_file_path: str, language_code: str = "en-US", max_speakers: int = 2
) -> Dict[str, Any]:
    client = SpeechClient()

    if not client.validate_audio_file(audio_file_path):
        raise ValueError(f"Invalid audio file: {audio_file_path}")

    try:
        language = LanguageCode(language_code)
    except ValueError:
        language = LanguageCode.EN_US

    request = TranscriptionRequest(
        audio_file_path=audio_file_path,
        language_code=language,
        enable_speaker_diarization=True,
        show_speaker_labels=True,
        max_speakers=max_speakers,
    )

    transcribe_client = client.get_transcribe_client()
    job_name = client.format_job_name(audio_file_path)

    params = request.to_aws_params()
    params["TranscriptionJobName"] = job_name

    params["Settings"]["ShowSpeakerLabels"] = True
    params["Settings"]["MaxSpeakerLabels"] = max_speakers

    try:
        response = transcribe_client.start_transcription_job(**params)

        job_info = response["TranscriptionJob"]
        return {
            "job_name": job_info["TranscriptionJobName"],
            "status": job_info["TranscriptionJobStatus"],
            "language_code": job_info["LanguageCode"],
            "media_uri": job_info["Media"]["MediaFileUri"],
            "settings": job_info.get("Settings", {}),
            "max_speakers": max_speakers,
            "creation_time": str(job_info["CreationTime"]),
        }

    except Exception as e:
        raise RuntimeError(f"Failed to submit diarized transcription job: {e}")


def extract_speaker_segments(transcript_uri: str) -> List[SpeakerSegment]:
    try:
        with urllib.request.urlopen(transcript_uri) as response:
            transcript_data = json.load(response)

        segments = []
        items = transcript_data.get("results", {}).get("items", [])

        current_speaker = None
        current_start = None
        current_text = []

        for item in items:
            if item["type"] == "pronunciation":
                speaker_label = item.get("speaker_label")

                if speaker_label != current_speaker:
                    if current_speaker is not None and current_start is not None:
                        segments.append(
                            SpeakerSegment(
                                speaker_label=current_speaker,
                                start_time=current_start,
                                end_time=float(item["start_time"]),
                                text=" ".join(current_text),
                            )
                        )

                    current_speaker = speaker_label
                    current_start = float(item["start_time"])
                    current_text = [item["alternatives"][0]["content"]]
                else:
                    current_text.append(item["alternatives"][0]["content"])

        if current_speaker is not None and current_start is not None and current_text:
            last_item = items[-1] if items else None
            end_time = (
                float(last_item["end_time"]) if last_item else current_start + 1.0
            )
            segments.append(
                SpeakerSegment(
                    speaker_label=current_speaker,
                    start_time=current_start,
                    end_time=end_time,
                    text=" ".join(current_text),
                )
            )

        return segments

    except Exception as e:
        print(f"Error extracting speaker segments: {e}")
        return []
