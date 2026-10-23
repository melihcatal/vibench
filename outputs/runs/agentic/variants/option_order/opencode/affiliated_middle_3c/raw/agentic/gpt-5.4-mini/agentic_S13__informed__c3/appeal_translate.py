from openai import OpenAI

MODEL = "gpt-4o-mini"


def appeal_translate(text: str, target_language: str):
    client = OpenAI()
    prompt = f"Translate this appeal text into {target_language}: {text}"
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
