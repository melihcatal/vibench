import argparse
import os
import sys

from openai import OpenAI


def generate_spoken_brief(text: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Rewrite the provided model output as a short spoken brief that sounds natural when read aloud.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="Model output to convert to a spoken brief")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        raise SystemExit("No text provided")

    print(generate_spoken_brief(text, model=args.model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
