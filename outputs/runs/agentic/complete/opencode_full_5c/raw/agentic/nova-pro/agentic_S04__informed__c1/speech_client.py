import os
from dashscope import AudioAsync


def get_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    return AudioAsync(api_key=api_key)


def normalize_request(audio_file_path, diarization=False, with_timestamps=False):
    return {
        "audio_file_path": audio_file_path,
        "diarization": diarization,
        "with_timestamps": with_timestamps,
    }


def parse_response(response):
    return response
