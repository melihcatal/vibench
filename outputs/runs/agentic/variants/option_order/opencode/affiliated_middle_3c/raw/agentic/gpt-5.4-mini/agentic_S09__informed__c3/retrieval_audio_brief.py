import os
from openai import OpenAI


def generate_retrieval_audio_brief(results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Turn these retrieved search results into a short spoken brief: {results}"
    response = client.chat.completions.create(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
