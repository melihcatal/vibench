import json
import urllib.request
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, LanguageCode, WordTimestamp


def request_timestamped_transcription(
    audio_file_path: str, language_code: str = "en-US"
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
        enable_word_timestamps=True,
    )

    transcribe_client = client.get_transcribe_client()
    job_name = client.format_job_name(audio_file_path)

    params = request.to_aws_params()
    params["TranscriptionJobName"] = job_name

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
        raise RuntimeError(f"Failed to submit timestamped transcription job: {e}")


def extract_word_timestamps(transcript_uri: str) -> List[WordTimestamp]:
    try:
        with urllib.request.urlopen(transcript_uri) as response:
            transcript_data = json.load(response)

        timestamps = []
        items = transcript_data.get("results", {}).get("items", [])

        for item in items:
            if item["type"] == "pronunciation":
                word = item["alternatives"][0]["content"]
                start_time = float(item["start_time"])
                end_time = float(item["end_time"])
                confidence = float(item["alternatives"][0].get("confidence", 0.0))

                timestamps.append(
                    WordTimestamp(
                        word=word,
                        start_time=start_time,
                        end_time=end_time,
                        confidence=confidence,
                    )
                )

        return timestamps

    except Exception as e:
        print(f"Error extracting word timestamps: {e}")
        return []


def get_segment_timestamps(
    transcript_uri: str, segment_duration: float = 30.0
) -> List[Dict[str, Any]]:
    try:
        with urllib.request.urlopen(transcript_uri) as response:
            transcript_data = json.load(response)

        segments = []
        items = transcript_data.get("results", {}).get("items", [])

        if not items:
            return segments

        current_segment_start = float(items[0]["start_time"])
        current_segment_text = []
        current_segment_words = []

        for item in items:
            if item["type"] == "pronunciation":
                word = item["alternatives"][0]["content"]
                start_time = float(item["start_time"])
                end_time = float(item["end_time"])

                if start_time - current_segment_start >= segment_duration:
                    segments.append(
                        {
                            "start_time": current_segment_start,
                            "end_time": float(items[items.index(item) - 1]["end_time"])
                            if items.index(item) > 0
                            else start_time,
                            "text": " ".join(current_segment_text),
                            "word_count": len(current_segment_words),
                        }
                    )

                    current_segment_start = start_time
                    current_segment_text = [word]
                    current_segment_words = [word]
                else:
                    current_segment_text.append(word)
                    current_segment_words.append(word)

        if current_segment_text:
            last_item = items[-1]
            segments.append(
                {
                    "start_time": current_segment_start,
                    "end_time": float(last_item["end_time"]),
                    "text": " ".join(current_segment_text),
                    "word_count": len(current_segment_words),
                }
            )

        return segments

    except Exception as e:
        print(f"Error extracting segment timestamps: {e}")
        return []
