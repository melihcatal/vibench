from openai import OpenAI

from identity_models import compact_text, response_payload


def onboarding_summary(state_text: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": compact_text(state_text)}],
    )
    content = completion.choices[0].message.content if completion.choices else ""
    return response_payload("OpenAI", "onboarding_summary", {"summary": content})
