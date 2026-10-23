from speech_client import SpeechClient


def request_diarization(audio_url: str) -> str:
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.
    """
    client = SpeechClient()
    params = {"speaker_labels": True}
    response = client.submit_job(audio_url, params=params)
    return response.get("id")
