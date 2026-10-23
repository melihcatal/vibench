from openai import OpenAI

client = OpenAI()


def reviewer_brief_audio(text, voice="alloy", model="gpt-5.4-mini"):
    resp = client.audio.speech.create(model=model, voice=voice, input=text)
    return resp.content
