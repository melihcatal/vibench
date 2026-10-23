from identity_client import IdentityClient


def onboarding_summary(state: str):
    client = IdentityClient.from_env()
    return client.post("/responses", {"model": "gpt-5.4-mini", "input": [{"state": state}]})
