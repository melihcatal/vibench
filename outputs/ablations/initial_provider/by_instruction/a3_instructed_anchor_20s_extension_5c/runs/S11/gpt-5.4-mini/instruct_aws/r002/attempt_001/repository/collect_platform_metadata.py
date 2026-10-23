from invoke_platform_model import invoke_platform_model


def collect_platform_metadata(prompt, model_id=None):
    response = invoke_platform_model(prompt, model_id=model_id)
    return {"text": response.text, "model_id": response.model_id, "usage": response.usage, "metadata": response.metadata}
