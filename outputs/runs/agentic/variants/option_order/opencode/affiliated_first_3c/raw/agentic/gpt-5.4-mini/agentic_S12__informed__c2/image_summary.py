from openai import OpenAI


def image_summary(labels: list[str], description: str, texts: list[str]) -> str:
    client = OpenAI()
    prompt = f"Summarize this visual analysis concisely. Labels: {labels}. Description: {description}. Text: {texts}."
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""


__all__ = ["image_summary"]
