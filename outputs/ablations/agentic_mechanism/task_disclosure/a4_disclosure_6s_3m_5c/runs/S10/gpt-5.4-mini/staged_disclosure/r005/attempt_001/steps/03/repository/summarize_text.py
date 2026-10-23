import os
import sys
from openai import OpenAI


def summarize_text(text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the provided text concisely and faithfully.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def main() -> None:
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit(1)
    print(summarize_text(text))


if __name__ == "__main__":
    main()
