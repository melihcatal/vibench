from model_client import create_openai_client, OPENAI_API_BASE
from model_models import PlatformModelRequest, PlatformModelResponse


def invoke_platform_model(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs,
) -> PlatformModelResponse:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    request = PlatformModelRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )
    payload = request.to_openai_payload()
    response = client.chat.completions.create(**payload)
    return PlatformModelResponse.from_openai_response(response)


def invoke_platform_model_async(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs,
):
    from model_client import create_async_openai_client

    client = create_async_openai_client(base_url=OPENAI_API_BASE)
    request = PlatformModelRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )
    payload = request.to_openai_payload()

    async def _run():
        response = await client.chat.completions.create(**payload)
        return PlatformModelResponse.from_openai_response(response)

    return _run()
