import os

from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = "Summarize these moderation decisions for a case worker: " + str(decisions)
    response = client.responses.create(model="gpt-4.1-mini", input=text)
    return response.output_text
