from identity_client import post_json


def onboarding_summary(state: dict) -> dict:
    return post_json("/responses", {"model": "gpt-5.4-mini", "input": state})
