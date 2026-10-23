import os

from openai import OpenAI


def onboarding_summary(state_text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize onboarding state for support: {state_text}",
    )
    return resp.output_text
