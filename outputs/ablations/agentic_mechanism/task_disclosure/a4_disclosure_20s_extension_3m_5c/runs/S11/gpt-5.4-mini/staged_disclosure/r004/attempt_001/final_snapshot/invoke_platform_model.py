import os
from typing import Any, Dict

from openai import OpenAI


def invoke_platform_model(prompt: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
    )
    return response.output_text


def main() -> None:
    prompt = os.environ.get("PROMPT", "Hello")
    print(invoke_platform_model(prompt))


if __name__ == "__main__":
    main()
