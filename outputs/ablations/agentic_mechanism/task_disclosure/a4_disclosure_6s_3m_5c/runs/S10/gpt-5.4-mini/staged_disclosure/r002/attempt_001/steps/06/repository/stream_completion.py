import os
from openai import OpenAI


def stream_completion(prompt: str, model: str = "gpt-4.1-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.responses.create(model=model, input=prompt, stream=True)
    for event in stream:
        if event.type == "response.output_text.delta":
            delta = getattr(event, "delta", None)
            if delta:
                print(delta, end="", flush=True)
        elif event.type == "response.completed":
            break


if __name__ == "__main__":
    import sys

    prompt_text = " ".join(sys.argv[1:]).strip()
    if not prompt_text:
        raise SystemExit("Usage: python stream_completion.py <prompt>")
    stream_completion(prompt_text)
