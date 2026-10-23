import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def localized_platform_output(raw_response: ModelInvocationResponse, target_locale: str) -> ModelInvocationResponse:
    """Translate model output into another locale using a translation service."""
    # Use Azure Translator Text API as example
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    if not endpoint or not key:
        raise RuntimeError("Translator credentials not configured")

    import requests
    url = f"{endpoint}/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = [{"Text": raw_response.output}]
    params = {
        "api-version": "3.0",
        "to": target_locale,
    }
    resp = requests.post(url, json=payload, headers=headers, params=params)
    resp.raise_for_status()
    translation = resp.json()[0]["translations"][0]["text"]
    # Return a new response with translated text, preserving original metadata.
    return ModelInvocationResponse(
        output=translation,
        usage=raw_response.usage,
        resource_id=raw_response.resource_id,
        metadata=raw_response.metadata,
    )


if __name__ == "__main__":
    # Example with Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_ID = "gpt-4o-mini"
    prompt = "What is the capital of France?"
    raw = ManagedModelClient().invoke(ModelInvocationRequest(DEPLOYMENT_ID, prompt))
    translated = localized_platform_output(raw, target_locale="es")
    print("Translated output:", translated.output)