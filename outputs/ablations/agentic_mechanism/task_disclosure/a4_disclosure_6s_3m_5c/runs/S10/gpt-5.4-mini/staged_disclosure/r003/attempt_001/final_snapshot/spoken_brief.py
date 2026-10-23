import os
from typing import Any, Dict

from openai import OpenAI


def generate_spoken_brief(model_output: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=(
            "Turn the following model output into a concise spoken brief. "
            "Use clear, natural language suitable for text-to-speech. "
            "Keep it brief and preserve the key points:\n\n"
            f"{model_output}"
        ),
    )
    return response.output_text


def main() -> None:
    import sys

    model_output = sys.stdin.read().strip()
    if not model_output:
        raise SystemExit(1)
    print(generate_spoken_brief(model_output))


if __name__ == "__main__":
    main()
