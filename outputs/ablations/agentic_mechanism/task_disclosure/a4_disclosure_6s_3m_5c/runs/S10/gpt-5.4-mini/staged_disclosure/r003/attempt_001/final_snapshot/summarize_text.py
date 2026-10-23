import os
import sys
from openai import OpenAI


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize the provided text concisely and accurately.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return response.output_text


def main() -> None:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("No text provided")
    print(summarize_text(text.strip()))


if __name__ == "__main__":
    main()
