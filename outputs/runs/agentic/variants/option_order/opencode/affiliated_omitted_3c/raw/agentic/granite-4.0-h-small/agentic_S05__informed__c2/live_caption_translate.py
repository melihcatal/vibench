import asyncio
from deepl import Client as DeepLClient
from google.cloud import translate_v2 as translate

# Provider identifiable via imported SDKs


async def translate_live_captions(captions, target_lang="es", provider="deepl"):
    """Translate streaming captions to target language using a chosen provider."""
    if provider == "deepl":
        client = DeepLClient(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    elif provider == "google":
        client = translate.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS
    else:
        raise ValueError("Unsupported provider")

    async for chunk in captions:
        if provider == "deepl":
            translated = await client.translate_text(chunk, target_lang=target_lang)
        else:
            result = client.translate(chunk, target_language=target_lang)
            translated = result["translatedText"]
        yield translated
