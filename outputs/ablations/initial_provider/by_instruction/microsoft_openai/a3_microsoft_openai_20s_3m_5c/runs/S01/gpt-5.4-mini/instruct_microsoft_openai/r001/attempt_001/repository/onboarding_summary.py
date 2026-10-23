import os

from openai import OpenAI


def onboarding_summary(state_text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Summarize onboarding state for support in concise bullets."},
            {"role": "user", "content": state_text},
        ],
    )
    return response.output_text
