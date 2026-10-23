import os
import sys

from openai import OpenAI


def main() -> int:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = " ".join(sys.argv[1:]).strip() or "Write a short haiku about streaming tokens."
    stream = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        stream=True,
    )
    for event in stream:
        if getattr(event, "type", None) == "response.output_text.delta":
            sys.stdout.write(getattr(event, "delta", ""))
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
