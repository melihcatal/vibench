from openai import OpenAI

from identity_client import openai_api_key
from identity_models import SummaryRequest


def onboarding_summary(account_id: str, state: dict):
    req = SummaryRequest(account_id=account_id, state=state)
    client = OpenAI(api_key=openai_api_key())
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize onboarding for account {req.account_id}: {req.state}",
    )
    return response.output_text
