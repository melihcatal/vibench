import json

from openai import OpenAI


def summarize_messages(text: str) -> dict:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this message processing result in one concise sentence:\n{text}")
    return {"summary": response.output_text}


if __name__ == "__main__":
    print(json.dumps(summarize_messages("processed 10 messages with 1 retry")))
