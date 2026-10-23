from model_client import get_client, get_model_name


def platform_output_safety(prompt: str, model: str = None):
    client = get_client()
    model_name = model or get_model_name()
    response = client.models.generate_content(model=model_name, contents=prompt)
    return getattr(response, "prompt_feedback", None)
