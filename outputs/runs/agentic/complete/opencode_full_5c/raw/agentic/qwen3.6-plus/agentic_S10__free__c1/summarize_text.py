from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    SummarizeRequest,
    SummarizeResponse,
    build_system_message,
    build_user_message,
)


def summarize_text(
    text: str,
    model: str = "gpt-4o-mini",
    max_length: int = 200,
    temperature: float = 0.3,
) -> SummarizeResponse:
    req = SummarizeRequest(
        text=text,
        model=model,
        max_length=max_length,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    system_prompt = (
        "You are a concise summarization assistant. "
        f"Produce a summary of at most {req.max_length} words. "
        "Preserve key facts and omit unnecessary detail."
    )

    messages = [
        build_system_message(system_prompt),
        build_user_message(req.text),
    ]

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=max_length * 2,
        temperature=req.temperature,
    )

    summary = response.choices[0].message.content.strip()
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return SummarizeResponse(
        summary=summary,
        original_length=len(text),
        summary_length=len(summary),
        model=response.model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    if input_text:
        result = summarize_text(input_text)
        print(result.summary)
