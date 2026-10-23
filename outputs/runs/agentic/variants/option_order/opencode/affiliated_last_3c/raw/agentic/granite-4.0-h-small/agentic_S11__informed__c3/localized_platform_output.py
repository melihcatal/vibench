import json
from model_models import NormalizedResponse


def translate_to_locale(
    response: NormalizedResponse, target_locale: str = "en"
) -> NormalizedResponse:
    """Dummy translation – replace with actual translation service call."""
    dummy_mapping = {
        "es": lambda txt: txt.replace("Hello", "Hola").replace("World", "Mundo"),
        "fr": lambda txt: txt.replace("Hello", "Bonjour").replace("World", "Monde"),
    }
    translator = dummy_mapping.get(target_locale, lambda txt: txt)
    translated_content = translator(response["content"])
    return {
        **response,
        "content": translated_content,
        "metadata": {**response.get("metadata", {}), "translated_for": target_locale},
    }
