from model_client import get_client, get_model_name


def localized_platform_output(prompt: str, target_locale: str, model: str = None):
    client = get_client()
    model_name = model or get_model_name()
    response = client.models.generate_content(
        model=model_name,
        contents=f"Translate to {target_locale}: {prompt}",
    )
    return response.text if hasattr(response, "text") else str(response)
