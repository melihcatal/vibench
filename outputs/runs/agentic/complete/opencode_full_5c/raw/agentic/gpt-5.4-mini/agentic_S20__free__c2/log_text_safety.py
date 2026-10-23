import os
from openai import OpenAI


def check_text(text: str) -> str:
    client = OpenAI()
    resp = client.moderations.create(model="omni-moderation-latest", input=text)
    return str(resp.results[0].flagged)


if __name__ == "__main__":
    print(check_text(os.getenv("LOG_TEXT", "")))
