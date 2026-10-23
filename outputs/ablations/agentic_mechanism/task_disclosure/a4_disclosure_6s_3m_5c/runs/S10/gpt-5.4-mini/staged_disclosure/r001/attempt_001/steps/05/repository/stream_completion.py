import os
import sys
from openai import OpenAI


def stream_completion(prompt: str) -> None:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        delta = event.choices[0].delta
        content = getattr(delta, "content", None)
        if content:
            sys.stdout.write(content)
            sys.stdout.flush()


if __name__ == "__main__":
    stream_completion(sys.stdin.read())
