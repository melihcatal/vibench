import os
from openai import OpenAI

def stream_platform_generation(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk.choices[0].delta.content or ""
