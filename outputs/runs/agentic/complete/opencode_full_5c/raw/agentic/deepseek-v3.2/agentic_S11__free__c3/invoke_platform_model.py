import os
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatRequest, ChatResponse


def invoke_platform_model(prompt: str, model_id: str = "gpt-4o") -> ChatResponse:
    """
    Invoke a provider-managed model through OpenAI's platform client.
    """
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )

        return ChatResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            raw_response=response,
        )
    except Exception as e:
        raise Exception(f"Failed to invoke OpenAI model {model_id}: {str(e)}")
