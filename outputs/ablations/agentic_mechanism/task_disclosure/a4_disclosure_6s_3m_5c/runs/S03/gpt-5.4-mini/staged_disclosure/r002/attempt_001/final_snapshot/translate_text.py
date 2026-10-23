import os
import sys
from openai import OpenAI


def translate_text(text: str, source_language: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": (
                    f"Translate the user's text from {source_language} to {target_language}. "
                    "Return only the translated text."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: translate_text.py <source_language> <target_language> <text>")
    source_language = sys.argv[1]
    target_language = sys.argv[2]
    text = " ".join(sys.argv[3:])
    print(translate_text(text, source_language, target_language))


if __name__ == "__main__":
    main()
