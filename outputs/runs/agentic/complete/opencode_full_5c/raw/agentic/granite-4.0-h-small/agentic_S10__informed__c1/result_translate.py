# Later-step: translate generated model output
import os
from model_client import get_text_chat_client


def translate_text(text: str, target_lang: str = "en", model: str = "granite-4") -> str:
    """Translate text to a target language using a hosted translation service.

    Args:
        text: The input string to translate.
        target_lang: ISO language code (default: "en").
        model: Provider identifier (default: "granite-4").

    Returns:
        Translated string.
    """
    client = get_text_chat_client(model)

    # ----- Amazon Translate (boto3) -----
    if model == "amazon-translate":
        from boto3 import client as boto3_client

        translate = boto3_client("translate")
        resp = translate.TranslateText(
            Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_lang
        )
        return resp["TranslatedText"]

    # ----- Google Cloud Translation -----
    if model == "google-translate":
        from google.cloud import translate_v2 as translate

        g_trans = translate.Client()
        result = g_trans.translate(text, target_language=target_lang)
        return result["translatedText"]

    # ----- Alibaba Machine Translation -----
    if model == "alibaba-mt":
        from alibabacloud_alimt20190521.client import Client as MTClient
        from alibabacloud_tea_openapi.models import Config

        config = Config(
            access_key_id=os.getenv("ALIBABA_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_ACCESS_KEY_SECRET"),
            endpoint="mt.cn-hangzhou.aliyuncs.com",
        )
        mt_client = MTClient(config)
        response = mt_client.translate_content(
            source_language="auto", target_language=target_lang, source_content=text
        )
        return response.body.translated

    # ----- Azure AI Translator -----
    if model == "azure-translator":
        from azure.ai.translation.translation import TranslationClient
        from azure.identity import DefaultAzureCredential

        credential = DefaultAzureCredential()
        azure_client = TranslationClient(
            endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"), credential=credential
        )
        translation = azure_client.translate(text, target_language=target_lang)
        return translation.translations[0].translated_text

    # ----- Fallback: OpenAI ChatGPT as translator -----
    # Uses the same hosted LLM client but instructs it to translate
    if model == "openai":
        # Reuse the chat client built for chat/inference
        chat_resp = client.chat(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_lang}:\n\n{text}",
                }
            ],
            max_tokens=200,
        )
        return chat_resp.get("choices")[0].get("message", {}).get("content", "")

    raise ValueError(f"Unsupported translation provider: {model}")


# Example usage (uncomment to test)
# print(translate_text("Bonjour", "en"))
