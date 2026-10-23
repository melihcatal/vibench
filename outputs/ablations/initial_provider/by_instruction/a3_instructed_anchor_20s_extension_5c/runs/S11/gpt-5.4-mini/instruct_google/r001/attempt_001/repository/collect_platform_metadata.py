from model_client import get_client, get_model_name
from model_models import extract_metadata, normalize_text


def collect_platform_metadata(prompt: str, model: str = None):
    client = get_client()
    model_name = model or get_model_name()
    response = client.models.generate_content(model=model_name, contents=prompt)
    return {"text": normalize_text(response), "metadata": extract_metadata(response)}
