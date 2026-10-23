import os

from openai import OpenAI


def main(logs):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize these error logs for incident review:\n{logs}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
