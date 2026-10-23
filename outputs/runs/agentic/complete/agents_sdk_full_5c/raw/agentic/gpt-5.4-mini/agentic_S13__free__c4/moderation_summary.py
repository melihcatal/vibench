from openai import OpenAI

from safety_client import get_openai_client


client: OpenAI = get_openai_client()
SUMMARY_MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: list[dict]) -> str:
    prompt = "Summarize these moderation decisions for an operations lead:\n" + str(decisions)
    response = client.responses.create(model=SUMMARY_MODEL, input=prompt)
    return response.output_text
