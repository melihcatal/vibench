from google import genai
from model_client import get_platform_client, get_platform_model_id
from model_models import normalize_platform_text


def localized_platform_output(text, target_locale="es"):
    client = get_platform_client()
    model_id = get_platform_model_id()
    response = client.models.generate_content(
        model=model_id,
        contents=f"Translate the following text to {target_locale} while preserving meaning: {normalize_platform_text(text)}",
    )
    return response.text if hasattr(response, "text") else str(response)
