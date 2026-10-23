from openai import OpenAI


def prompt_safety(text: str) -> str:
    client = OpenAI()
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    return "unsafe" if moderation.results and moderation.results[0].flagged else "safe"
