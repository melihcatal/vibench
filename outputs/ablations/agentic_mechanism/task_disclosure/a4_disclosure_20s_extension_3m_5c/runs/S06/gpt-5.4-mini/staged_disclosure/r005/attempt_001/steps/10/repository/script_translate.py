import os
from openai import OpenAI


def translate_script(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Translate narration scripts for synthesis. Preserve meaning, tone, punctuation, line breaks, and speaker labels.",
            },
            {
                "role": "user",
                "content": f"Translate the following script to {target_language}:\n\n{text}",
            },
        ],
    )
    return response.output_text.strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: script_translate.py <text> [target_language]")
    target = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_script(sys.argv[1], target))
