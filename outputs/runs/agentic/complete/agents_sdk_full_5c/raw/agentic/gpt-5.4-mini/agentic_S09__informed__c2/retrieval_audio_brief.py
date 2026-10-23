import os

from openai import OpenAI


AUDIO_BRIEF_MODEL = "gpt-4o-mini"
AUDIO_PROVIDER = "OpenAI TTS via chat brief generation"


def generate_spoken_brief(results):
    client = OpenAI()
    joined = "\n".join(f"- {item}" for item in results)
    prompt = f"Create a concise spoken brief for these retrieved results:\n{joined}"
    completion = client.chat.completions.create(
        model=AUDIO_BRIEF_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content
