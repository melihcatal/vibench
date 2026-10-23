from openai import OpenAI


def appeal_translate(text, target_language="en"):
    client = OpenAI()
    prompt = f"Translate this appeal text to {target_language}: {text}"
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
