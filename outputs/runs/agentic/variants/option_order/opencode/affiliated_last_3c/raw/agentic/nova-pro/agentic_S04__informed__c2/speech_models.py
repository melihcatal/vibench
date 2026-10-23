from .speech_client import get_speech_client


# Define local request, response, and normalization helpers for Batch Speech-to-Text
def normalize_transcription_result(result):
    return result.text


def format_transcription_request(audio_file_path):
    return {"audio_file_path": audio_file_path}
