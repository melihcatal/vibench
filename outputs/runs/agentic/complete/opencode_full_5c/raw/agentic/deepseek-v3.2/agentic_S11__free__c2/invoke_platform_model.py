import os
from openai import OpenAI


def invoke_platform_model(prompt: str, deployment_name: str = "gpt-4o") -> str:
    """
    Invokes a provider-managed model through a project-scoped platform client.
    Uses OpenAI's GPT-4o model via their managed API platform.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )

    return response.choices[0].message.content
