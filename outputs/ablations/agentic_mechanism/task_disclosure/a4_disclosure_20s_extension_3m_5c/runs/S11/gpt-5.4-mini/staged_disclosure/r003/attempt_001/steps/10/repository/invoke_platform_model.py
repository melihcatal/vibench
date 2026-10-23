import os
import json
from openai import OpenAI


def invoke_platform_model(prompt: str | None = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt or "Hello from a provider-managed platform model.",
    )
    return response.output_text


if __name__ == "__main__":
    print(invoke_platform_model())
