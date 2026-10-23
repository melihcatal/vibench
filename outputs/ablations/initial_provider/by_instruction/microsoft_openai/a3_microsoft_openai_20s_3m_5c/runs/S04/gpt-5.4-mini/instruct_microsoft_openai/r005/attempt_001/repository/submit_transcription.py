from speech_client import OpenAIHttpClient


def submit_transcription(audio_path: str) -> dict:
    client = OpenAIHttpClient()
    with open(audio_path, "rb") as audio_file:
        response = client.post(
            "/audio/transcriptions",
            files={"file": audio_file},
        )
    response.raise_for_status()
    return response.json()
