from .speech_client import get_transcription_client


def normalize_transcription_response(response):
    client = get_transcription_client()
    # Additional logic to normalize transcription response
    return "Normalized response"
