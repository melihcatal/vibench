from google import genai
from model_client import get_platform_client, get_platform_model_id, get_platform_resource_name
from model_models import PlatformResourceSelection, normalize_platform_text


def select_platform_resource(query=None, prefer_model=True):
    client = get_platform_client()
    model_id = get_platform_model_id()
    resource_name = get_platform_resource_name()
    selection = PlatformResourceSelection(query=normalize_platform_text(query or resource_name), model_id=model_id, resource_name=resource_name)
    if prefer_model:
        model = client.models.get(model=model_id)
        return {"selection": selection.to_dict(), "resource": model}
    response = client.models.generate_content(
        model=model_id,
        contents=f"Resolve the best platform resource for: {selection.query}",
    )
    return {"selection": selection.to_dict(), "resource": response}
