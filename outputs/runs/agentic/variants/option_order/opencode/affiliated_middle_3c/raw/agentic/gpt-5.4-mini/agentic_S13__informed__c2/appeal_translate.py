from openai import OpenAI


def appeal_translate(text, target_language="en", model="gpt-4o-mini"):
    client = OpenAI()
    prompt = f"Translate this appeal text into {target_language}: {text}"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
