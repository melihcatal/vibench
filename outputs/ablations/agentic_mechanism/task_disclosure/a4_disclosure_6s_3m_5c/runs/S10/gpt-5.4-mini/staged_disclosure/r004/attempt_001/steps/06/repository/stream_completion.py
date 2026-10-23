import os
import sys

from openai import OpenAI


def stream_completion(prompt: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
        stream=True,
    )
    collected = []
    for event in stream:
        event_type = getattr(event, "type", None)
        if event_type == "response.output_text.delta":
            delta = getattr(event, "delta", "")
            if delta:
                collected.append(delta)
                sys.stdout.write(delta)
                sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(collected)


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        raise SystemExit("usage: python stream_completion.py <prompt>")
    stream_completion(prompt)
