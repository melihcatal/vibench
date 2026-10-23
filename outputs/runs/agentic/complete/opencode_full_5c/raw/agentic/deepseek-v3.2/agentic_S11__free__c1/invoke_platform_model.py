import os
from openai import OpenAI
from model_client import get_platform_client
from model_models import PlatformRequest, PlatformResponse


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    """Invoke a provider-managed model through a project-scoped platform client."""
    client = get_platform_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_message},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )

        return PlatformResponse(
            content=response.choices[0].message.content,
            model_id=response.model,
            usage=response.usage,
            raw_response=response,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to invoke OpenAI model: {str(e)}")
