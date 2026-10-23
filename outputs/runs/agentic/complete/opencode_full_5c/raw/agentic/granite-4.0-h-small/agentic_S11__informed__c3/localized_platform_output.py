# localized_platform_output.py
# LATER-STEP: translates platform model output into another locale

from model_client import get_provider_client
from model_models import parse_response


def translate_output(text: str, target_locale: str = "fr-FR") -> str:
    """Translate model output using a hosted translation provider."""
    if target_locale == "en-US":
        # No translation needed
        return text
    provider = infer_provider_name()
    if provider == "aws":
        client = get_provider_client("aws")
        # Amazon Translate call (boto3)
        response = client.translate_text(
            Text=text, SourceLanguageCode="en", TargetLanguageCode=target_locale
        )
        return response["TranslatedText"]
    elif provider == "azure_openai":
        # Azure Translator SDK usage
        client = get_provider_client("azure")
        translation = client.translate([text], target_language=target_locale)[0][
            "translations"
        ][0]["text"]
        return translation
    elif provider == "gcp":
        client = get_provider_client("gcp")
        translation = client.translate(text, target_language=target_locale)[
            "translatedText"
        ]
        return translation
    # Add additional providers here
    raise NotImplementedError(f"Translation not implemented for provider {provider}")
