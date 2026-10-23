from openai import OpenAI

client = OpenAI()


def appeal_translate(text, target_language="en", model="gpt-5.4-mini"):
    prompt = f"Translate this appeal text to {target_language}: {text}"
    resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content
