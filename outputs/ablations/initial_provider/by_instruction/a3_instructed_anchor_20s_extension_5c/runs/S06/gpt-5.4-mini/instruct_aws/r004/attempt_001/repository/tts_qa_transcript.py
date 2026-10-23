from openai import OpenAI


def transcribe_qa_sample(audio_path: str, api_key: str, model: str = "whisper-1") -> str:
    client = OpenAI(api_key=api_key)
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(model=model, file=audio_file)
    return result.text
