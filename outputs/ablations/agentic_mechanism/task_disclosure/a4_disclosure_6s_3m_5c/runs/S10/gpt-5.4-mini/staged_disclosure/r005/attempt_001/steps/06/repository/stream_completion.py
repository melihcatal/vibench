import os
from openai import OpenAI


def stream_completion(prompt: str, model: str = "gpt-4.1-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.responses.create(model=model, input=prompt, stream=True)
    for event in stream:
        if event.type == "response.output_text.delta":
            yield event.delta


if __name__ == "__main__":
    import sys

    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        raise SystemExit(1)
    for token in stream_completion(prompt):
        print(token, end="", flush=True)
