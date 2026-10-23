from openai import OpenAI


def onboarding_summary(state: str):
    client = OpenAI()
    resp = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": state}])
    return resp.choices[0].message.content
