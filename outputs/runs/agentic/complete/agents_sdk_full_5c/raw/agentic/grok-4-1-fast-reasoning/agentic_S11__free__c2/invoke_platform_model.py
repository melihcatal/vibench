from model_client import get_platform_client

def invoke_platform_model(prompt: str, deployment: str = "gpt-4o-mini-deployment") -> str:
    client = get_platform_client()
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content