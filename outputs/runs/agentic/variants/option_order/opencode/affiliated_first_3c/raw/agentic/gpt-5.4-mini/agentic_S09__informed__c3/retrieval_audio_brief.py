from openai import OpenAI


def retrieval_audio_brief(results) -> bytes:
    client = OpenAI()
    text = "
".join(str(item) for item in results)
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return speech.read()
