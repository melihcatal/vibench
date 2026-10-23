from openai import OpenAI
import os

def stream_model_generation(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk.choices[0].delta.content or ""
