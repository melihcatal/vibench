import os

from openai import OpenAI


def onboarding_summary(state: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this onboarding state for support in one concise paragraph: {state}",
    )
    return response.output_text
