from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI()
    return client.responses.create(model="gpt-5.4-mini", input=f"Summarize moderation decisions: {decisions}")
