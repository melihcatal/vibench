import os
from typing import Dict

from openai import OpenAI

from security_models import build_metadata, normalize_text


def payload_safety(text: str) -> Dict[str, object]:
    client = OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest", input=normalize_text(text)
    )
    result = response.results[0]
    return {
        "provider": "openai_moderation",
        "unsafe": bool(result.flagged),
        "metadata": build_metadata(categories=getattr(result, "categories", None)),
    }


def main() -> None:
    text = os.getenv("PLAINTEXT", "")
    print(payload_safety(text))


if __name__ == "__main__":
    main()
