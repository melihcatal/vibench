import os
import sys
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI


@dataclass(frozen=True)
class SafetyIssue:
    label: str
    severity: str
    excerpt: str


def load_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_narration_script(text: str) -> str:
    client = load_client()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You inspect narration scripts for unsafe content. Flag self-harm, violence, hate, sexual content involving minors, illegal wrongdoing, extremism, harassment, privacy leakage, and dangerous instructions. Return concise findings only.",
            },
            {
                "role": "user",
                "content": f"Review this narration script for unsafe content and return a short safety report:\n\n{text}",
            },
        ],
    )
    return response.output_text


def read_input(path: Optional[str]) -> str:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> None:
    if len(sys.argv) > 2:
        raise SystemExit("Usage: script_safety.py [input_file|-]")
    input_path = sys.argv[1] if len(sys.argv) == 2 else None
    text = read_input(input_path)
    sys.stdout.write(check_narration_script(text))


if __name__ == "__main__":
    main()
