from model_client import client


def invoke_platform_model(prompt: str) -> Dict[str, Any]:
    response = client.generate_text(prompt=prompt)
    return response
