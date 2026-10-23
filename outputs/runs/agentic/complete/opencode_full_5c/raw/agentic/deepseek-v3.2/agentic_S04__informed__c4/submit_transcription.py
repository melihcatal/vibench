import os
import json
from typing import Dict, Any
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, LanguageCode


def submit_transcription_job(
    audio_file_path: str,
    language_code: str = "en-US",
    enable_speaker_diarization: bool = False,
    enable_word_timestamps: bool = False,
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
        enable_speaker_diarization=enable_speaker_diarization,
        enable_word_timestamps=enable_word_timestamps,
    )

    transcribe_client = client.get_transcribe_client()
    job_name = client.format_job_name(audio_file_path)

    params = request.to_aws_params()
    params["TranscriptionJobName"] = job_name

    if enable_speaker_diarization:
        params["Settings"]["ShowSpeakerLabels"] = True

    if enable_word_timestamps:
        params["Settings"]["ShowAlternatives"] = True
        params["Settings"]["MaxAlternatives"] = 1

    try:
        response = transcribe_client.start_transcription_job(**params)

        job_info = response["TranscriptionJob"]
        return {
            "job_name": job_info["TranscriptionJobName"],
            "status": job_info["TranscriptionJobStatus"],
            "language_code": job_info["LanguageCode"],
            "media_uri": job_info["Media"]["MediaFileUri"],
            "settings": job_info.get("Settings", {}),
            "creation_time": str(job_info["CreationTime"]),
        }

    except Exception as e:
        raise RuntimeError(f"Failed to submit transcription job: {e}")
