import os
import sys
from openai import OpenAI


def translate_script(text: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        f"Translate the following narration script into {target_language}. "
        "Preserve meaning, tone, punctuation, line breaks, and speaker cues. "
        "Return only the translated script.\n\n"
        f"{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional translation engine."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: script_translate.py <input_text> [target_language]")
    input_text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "English"
    print(translate_script(input_text, target_language))


if __name__ == "__main__":
    main()
