# localized_platform_output.py
# LATER-STEP
# Translate platform model output for another locale

from model_models import ModelInvocationResponse
from typing import Literal

# Stub translator; replace with real translation service (e.g., Google Translate API)

def translate(text: str, target: Literal["es", "fr", "de"] = "es") -> str:
    # Dummy translation: append language code for illustration
    return f"[Translated to {target}]: {text}"


def localize(response: ModelInvocationResponse, target_lang: Literal["es", "fr", "de"] = "es") -> ModelInvocationResponse:
    localized_text = translate(response.output, target=target_lang)
    # Keep original usage metadata
    return ModelInvocationResponse(output=localized_text, usage=response.usage)

# Example usage stub
if __name__ == "__main__";
    original = ModelInvocationResponse(output="Hello world!", usage={})
    print(localize(original, target_lang="fr").output)
