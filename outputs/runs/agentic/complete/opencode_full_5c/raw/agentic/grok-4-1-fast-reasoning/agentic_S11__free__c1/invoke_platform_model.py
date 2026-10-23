from model_client import get_platform_client


def invoke_platform_model(prompt: str, deployment_id: str) -> str:
    """
    Invokes an Azure OpenAI model deployment via project-scoped client.
    """
    client = get_platform_client()
    response = client.chat.completions.create(
        model=deployment_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content
