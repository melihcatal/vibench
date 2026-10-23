# localized_platform_output.py
# [LATER-STEP]
# Translate platform model output for another locale

from model_client import ManagedModelClient
from model_models import (
    ModelInvocationResponse,
    LocalizationRequest,
    LocalizationResponse,
)

# Dummy locale map (in production use a translation service like DeepL or Google Translate)
LOCALE_MAP = {
    "es": "Hola",
    "fr": "Bonjour",
    "de": "Hallo",
}


def translate_output(
    invocation: ModelInvocationResponse, target_locale: str
) -> LocalizationResponse:
    """Translate the output text using a concrete provider (e.g., OpenAI translation)."""
    client = ManagedModelClient(provider="openai")
    # Pretend we have a translation model; in real code call the translation API
    translation = LOCALE_MAP.get(target_locale, invocation.output_text)
    # Build a response object preserving original metadata
    result = LocalizationResponse(
        locale=target_locale,
        translated_text=translation,
        original_response=invocation,
    )
    return result


@dataclass
class LocalizationRequest:
    source_locale: str = "en"
    target_locale: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LocalizationResponse:
    locale: str
    translated_text: str
    original_response: Optional[ModelInvocationResponse] = None

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["original_response"] = (
            out["original_response"].to_dict() if out["original_response"] else None
        )
        del out["original_response"]  # flatten when nested
        return out


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     original = ModelInvocationResponse(run_id="1", output_text="Hello", usage=None)
#     loc = translate_output(original, target_locale="fr")
#     print(loc.to_dict())
