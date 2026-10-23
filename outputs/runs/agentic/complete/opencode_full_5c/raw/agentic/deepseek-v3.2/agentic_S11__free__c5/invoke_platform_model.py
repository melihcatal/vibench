import os
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatRequest, ChatResponse


def invoke_platform_model(prompt: str, model: str = "gpt-4o") -> ChatResponse:
    """Invoke a provider-managed model through a project-scoped platform client."""
    client = get_openai_client()

    # Use OpenAI's chat completion API with provider-specific model identifier
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )

    # Extract provider-specific response data
    content = response.choices[0].message.content
    usage = response.usage

    return ChatResponse(
        content=content, model=model, usage=usage, raw_response=response
    )


if __name__ == "__main__":
    # Example usage
    result = invoke_platform_model("Explain quantum computing in simple terms.")
    print(f"Response: {result.content[:100]}...")
    print(f"Model: {result.model}")
    print(f"Usage: {result.usage}")
