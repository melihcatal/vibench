from openai import OpenAI


def onboarding_summary(state_text: str):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this onboarding state for support: {state_text}")
    return response.output_text
