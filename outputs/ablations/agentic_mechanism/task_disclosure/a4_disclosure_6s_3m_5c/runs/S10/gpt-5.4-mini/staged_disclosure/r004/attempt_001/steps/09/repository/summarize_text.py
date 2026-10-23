import os
import sys
import argparse

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
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="Text to summarize")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        raise SystemExit("No text provided")

    print(summarize_text(text, model=args.model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
