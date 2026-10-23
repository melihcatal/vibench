from model_client import HostedLLMClient
from model_models import LLMRequest, ModelConfig, normalize_messages


SYSTEM_PROMPT = (
    "You are a concise summarization assistant. "
    "Read the provided text and produce a clear, accurate summary that captures the main points. "
    "Keep the summary proportional to the input length."
)


def summarize_text(
    text: str,
    max_words: int = 150,
    model: str = "gpt-4o",
    temperature: float = 0.5,
    config: ModelConfig | None = None,
) -> str:
    client = HostedLLMClient(config=config)
    user_content = (
        f"Summarize the following text in approximately {max_words} words:\n\n{text}"
    )
    messages = normalize_messages(user_content, system_prompt=SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_words * 2,
    )
    response = client.chat_completion(request)
    return response.content


if __name__ == "__main__":
    import sys

    sample = (
        sys.stdin.read()
        if not sys.stdin.isatty()
        else (
            "Large language models have transformed natural language processing by enabling "
            "few-shot and zero-shot learning across diverse tasks. These models, trained on "
            "massive corpora of text, demonstrate emergent capabilities that were not explicitly "
            "programmed. Applications include translation, summarization, question answering, "
            "and code generation. However, challenges remain around factual accuracy, bias, "
            "computational cost, and safe deployment in production systems."
        )
    )
    result = summarize_text(sample)
    print(result)
