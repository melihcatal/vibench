import os
from openai import OpenAI

MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Turn these retrieved search results into a short spoken brief:
{results}"
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
