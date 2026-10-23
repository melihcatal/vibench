import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

# Translation service configuration (Azure AI Translator used as example)
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "global")
TARGET_LOCALE = os.getenv("TARGET_LOCALE", "es")  # default Spanish


async def translate_output(
    model_response: ModelInvocationResponse, target_locale: str = TARGET_LOCALE
) -> ModelInvocationResponse:
    """
    Translate the raw model output into another locale using Azure AI Translator SDK.
    Returns a new ModelInvocationResponse where `output` is replaced with the translated text.
    ","""
    # Placeholder: add `azure-ai-translation-text` and use `TranslationClient`
    # from azure.ai.translation.text import TranslationClient
    # client = TranslationClient(endpoint=AZURE_TRANSLATOR_ENDPOINT, credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY))
    # translation = await client.translate(text=model_response.output, target_language=target_locale)
    # For demo, we simulate translation by appending locale tag.
    translated = f"[Translated to {target_locale.upper()}]: {model_response.output}"
    return ModelInvocationResponse(
        output=translated,
        usage=model_response.usage,
        resource_id=model_response.resource_id,
        metadata={
            **(model_response.metadata or {}),
            "translation": {
                "target_locale": target_locale,
                "original_length": len(model_response.output),
            },
        },
    )


if __name__ == "__main__":

    async def demo():
        payload = {
            "messages": [
                {"role": "user", "content": "Explain the water cycle in simple terms."}
            ],
            "temperature": 0.3,
            "max_tokens": 80,
        }
        request = ModelInvocationRequest(**payload)
        client = ManagedModelClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        )
        raw_resp = await client.generate(
            payload["messages"],
            payload["temperature"],
            payload["max_tokens"],
        )
        raw_resp = raw_resp  # type: ignore
        resp = ModelInvocationResponse(
            output=raw_resp.get("choices")[0].get("message").get("content"),
            usage=raw_resp.get("usage"),
            resource_id=raw_resp.get("id"),
            metadata=raw_resp.get("metadata", {}),
        )
        translated_resp = await translate_output(resp, target_locale="fr")
        print(
            json.dumps(
                {"original": resp.output, "translated": translated_resp.output},
                indent=2,
            )
        )

    asyncio.run(demo())
