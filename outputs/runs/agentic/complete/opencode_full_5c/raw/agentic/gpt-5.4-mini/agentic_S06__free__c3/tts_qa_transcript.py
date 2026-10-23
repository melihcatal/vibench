from openai import OpenAI


def transcribe_tts_sample(audio_bytes: bytes, filename: str = "sample.mp3") -> str:
    client = OpenAI()
    from io import BytesIO

    file_obj = BytesIO(audio_bytes)
    file_obj.name = filename
    response = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe", file=file_obj
    )
    return response.text
