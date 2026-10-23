from model_models import ModelRequest, ModelResponse
from model_client import create_chat_completion


def summarize_text(
    text: str, max_words: int = 150, model: str = "gpt-4o"
) -> ModelResponse:
    system_prompt = (
        "You are a professional summarization assistant. "
        "Provide a concise, accurate summary that captures the key points. "
        f"Keep the summary under {max_words} words."
    )

    request = ModelRequest(
        prompt=text,
        system_prompt=system_prompt,
        model=model,
        temperature=0.3,
        max_tokens=512,
    )

    return create_chat_completion(request, default_system=system_prompt)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = summarize_text(input_text)
    print(result.text)
