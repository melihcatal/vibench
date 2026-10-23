from openai import OpenAI


def translate_appeal(
    text: str, target_language: str = "en", model: str = "gpt-5.4-mini"
):
    client = OpenAI()
    prompt = f"Translate this appeal text to {target_language}: {text}"
    result = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content
