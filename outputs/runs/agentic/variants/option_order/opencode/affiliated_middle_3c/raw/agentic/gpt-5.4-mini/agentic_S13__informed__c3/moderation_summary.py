from openai import OpenAI

MODEL = "gpt-5.4-mini"


def moderation_summary(decisions: list[dict]):
    client = OpenAI()
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": str(decisions)}])
    return response.choices[0].message.content
