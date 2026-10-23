from openai import OpenAI


def transcribe_qa_audio(audio_path: str) -> str:
    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )
    return response.text
