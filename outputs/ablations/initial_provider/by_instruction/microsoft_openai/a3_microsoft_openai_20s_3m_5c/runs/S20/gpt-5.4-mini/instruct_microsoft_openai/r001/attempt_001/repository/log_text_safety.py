import os

from openai import OpenAI


def main() -> dict:
    client = OpenAI()
    text = os.getenv("LOG_TEXT", "")
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return {"flagged": response.results[0].flagged, "categories": response.results[0].categories.model_dump()}


if __name__ == "__main__":
    main()
