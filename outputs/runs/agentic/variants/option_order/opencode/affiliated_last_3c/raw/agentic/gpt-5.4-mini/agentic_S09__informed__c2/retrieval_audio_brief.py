import os

from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = " ".join(str(item) for item in results)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize briefly: {text}"}],
    )
    return response.choices[0].message.content
