from openai import OpenAI
import os


def spoken_brief(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=os.getenv("OPENAI_TTS_SCRIPT_MODEL", "gpt-4.1-mini"), messages=[{"role": "system", "content": "Rewrite this as a short spoken brief."}, {"role": "user", "content": text}], temperature=0.4, max_tokens=180)
    return response.choices[0].message.content or ""
