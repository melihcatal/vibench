from model_models import ModelRequest, StreamChunk
from model_client import stream_chat_completion


def stream_completion(
    prompt: str,
    context: str = "",
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 2048,
):
    request = ModelRequest(
        prompt=prompt,
        context=context if context else None,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    accumulated = ""
    for chunk in stream_chat_completion(request):
        accumulated += chunk.text
        yield chunk

    return accumulated


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    full_text = ""
    for chunk in stream_completion(input_text):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_text += chunk.text
    print()
