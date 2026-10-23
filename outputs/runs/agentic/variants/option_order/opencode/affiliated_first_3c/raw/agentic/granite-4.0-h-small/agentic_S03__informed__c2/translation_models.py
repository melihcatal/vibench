from ibm_watsonx_ai.services.translation import TranslationService
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Models supported by the translation service
SupportedModels = {
    "DeeplAuthKey": os.getenv("DEEPL_AUTH_KEY"),
    "GoogleTranslateKey": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
}


def supported_model(model: str):
    """Return the auth configuration for a given translation model."""
    # Placeholder: mapping model name to actual auth config; extend as needed.
    pass
