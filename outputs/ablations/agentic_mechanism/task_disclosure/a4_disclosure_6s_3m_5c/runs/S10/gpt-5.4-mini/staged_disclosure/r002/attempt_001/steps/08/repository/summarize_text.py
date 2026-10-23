import os
import sys
from openai import OpenAI


def summarize_text(text: str, max_output_tokens: int = 200) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the user's text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
        max_output_tokens=max_output_tokens,
    )
    return response.output_text


def _read_text_from_args() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    return sys.stdin.read()


def main() -> None:
    text = _read_text_from_args().strip()
    if not text:
        raise SystemExit("No input text provided")
    print(summarize_text(text))


if __name__ == "__main__":
    main()
