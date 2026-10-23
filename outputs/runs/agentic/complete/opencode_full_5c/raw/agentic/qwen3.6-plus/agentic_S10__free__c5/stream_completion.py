from model_client import HostedLLMClient
from model_models import LLMRequest, ModelConfig, normalize_messages


SYSTEM_PROMPT = "You are a helpful assistant. Provide clear and detailed responses."


def stream_completion(
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    config: ModelConfig | None = None,
) -> str:
    client = HostedLLMClient(config=config)
    messages = normalize_messages(prompt, system_prompt=SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    accumulated = []
    for chunk in client.stream_completion(request):
        accumulated.append(chunk.delta)
        yield chunk.delta
    yield "".join(accumulated)


def stream_completion_full(
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    config: ModelConfig | None = None,
) -> str:
    client = HostedLLMClient(config=config)
    messages = normalize_messages(prompt, system_prompt=SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    accumulated = []
    for chunk in client.stream_completion(request):
        accumulated.append(chunk.delta)
    return "".join(accumulated)


if __name__ == "__main__":
    prompt = "Write a short paragraph about the benefits of renewable energy."
    print("Streaming tokens:")
    for token in stream_completion(prompt):
        print(token, end="", flush=True)
    print()
