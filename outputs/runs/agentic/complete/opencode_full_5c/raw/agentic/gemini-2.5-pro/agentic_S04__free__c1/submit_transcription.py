from speech_client import SpeechClient


def submit_transcription(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    client = SpeechClient()
    response = client.submit_job(audio_url)
    return response.get("id")
