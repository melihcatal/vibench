from typing import Dict, Any

def create_recognition_config(language_code: str, enable_speaker_diarization: bool = False, enable_word_time_offsets: bool = False) -> Dict[str, Any]:
    config = {
        "language_code": language_code,
    }
    if enable_speaker_diarization:
        config["enable_speaker_diarization"] = True
        config["diarization_speaker_count"] = 2 # Default to 2 speakers
    if enable_word_time_offsets:
        config["enable_word_time_offsets"] = True
    return config

def create_recognition_audio(audio_uri: str) -> Dict[str, Any]:
    return {
        "uri": audio_uri
    }

def normalize_transcript_result(operation_name: str, response: Dict[str, Any]) -> Dict[str, Any]:
    # Basic normalization, could be expanded based on specific needs
    return {
        "job_id": operation_name,
        "status": "COMPLETED" if response.get("done") else "IN_PROGRESS",
        "transcript": response.get("response", {}).get("results", [])
    }
