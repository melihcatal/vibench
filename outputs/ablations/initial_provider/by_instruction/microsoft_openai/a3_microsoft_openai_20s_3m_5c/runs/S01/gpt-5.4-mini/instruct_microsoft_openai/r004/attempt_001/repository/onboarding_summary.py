from identity_client import openai_headers, post_json


def onboarding_summary(state_text: str):
    payload = {"model": "gpt-5.4-mini", "input": f"Summarize onboarding state for support: {state_text}"}
    return post_json("https://api.openai.com/v1/responses", payload, headers=openai_headers())
