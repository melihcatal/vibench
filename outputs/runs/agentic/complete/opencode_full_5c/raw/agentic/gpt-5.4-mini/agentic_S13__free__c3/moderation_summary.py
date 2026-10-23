import os
from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "Summarize moderation decisions concisely: " + str(decisions)
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
