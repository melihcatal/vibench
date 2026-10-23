from model_models import collect_metadata, normalize_text
from invoke_platform_model import invoke_platform_model


def collect_platform_metadata(prompt: str, resource: str = None):
    response = invoke_platform_model(prompt, resource)
    text = normalize_text(
        getattr(response, "output_text", None) or getattr(response, "output", None)
    )
    metadata = collect_metadata(response, ["id", "model", "usage", "created_at"])
    return {"text": text, "metadata": metadata, "raw": response}
