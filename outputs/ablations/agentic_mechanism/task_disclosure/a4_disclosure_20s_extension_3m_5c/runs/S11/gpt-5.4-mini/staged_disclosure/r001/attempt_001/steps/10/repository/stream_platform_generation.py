import os
from typing import Iterator, Any

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def stream_generation(prompt: str) -> Iterator[Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with client.responses.stream(model=MODEL_ID, input=prompt) as stream:
        for event in stream:
            yield event
        yield stream.get_final_response()


def main() -> None:
    prompt = os.getenv("PROMPT", "Hello")
    for item in stream_generation(prompt):
        print(item)


if __name__ == "__main__":
    main()
