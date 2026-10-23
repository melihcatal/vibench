from collections import Counter

from openai import OpenAI


def message_summary(messages: list[str]) -> str:
    client = OpenAI()
    joined = "\n".join(messages[:20])
    prompt = f"Summarize these message processing results briefly:\n{joined}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
