from openai import OpenAI


def runbook_translate(
    text: str, target_language: str = "es", model: str = "gpt-5.4-mini"
):
    client = OpenAI()
    prompt = (
        f"Translate the following secret-rotation runbook to {target_language}: {text}"
    )
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
