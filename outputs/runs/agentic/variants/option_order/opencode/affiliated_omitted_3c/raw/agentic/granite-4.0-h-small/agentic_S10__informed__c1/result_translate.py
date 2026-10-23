import boto3
import requests
import json
import deepl


def translate(text: str, target_lang: str = "en", provider: str = "aws") -> str:
    """Translate generated model output to a target language using a hosted translation service.

    Args:
        text (str): The output to translate.
        target_lang (str): Target language code (ISO 639-1, e.g., 'fr', 'de').
        provider (str): One of 'aws' (Amazon Translate), 'alibaba', 'deepl', 'google', 'azure'.

    Returns:
        str: Translated text.
    """
    if provider == "aws":
        client = boto3.client("translate", region_name="us-east-1")
        response = client.translate_text(
            Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_lang
        )
        return response["TranslatedText"]
    elif provider == "alibaba":
        client = alibabacloud_alimt.AliyunMPSClient(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
        response = client.translate(
            src_text=text, source_lang="auto", target_lang=target_lang
        )
        return response["translated"]
    elif provider == "deepl":
        client = deepl.DeepL(auth_key=os.getenv("DEEPL_AUTH_KEY"))
        translation = client.translate_text(text, target_lang=target_lang)
        return translation.text
    elif provider == "google":
        client = google.cloud.translate_v2.Client()
        result = client.translate(text, target_language=target_lang)
        return result["translatedText"]
    elif provider == "azure":
        endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
        key = os.getenv("AZURE_TRANSLATOR_KEY")
        headers = {"Ocp-Apim-Subscription-Key": key}
        payload = {"Texts": [text]}
        r = requests.post(
            f"{endpoint}/translate?api-version=3.0&to={target_lang}",
            headers=headers,
            json=payload,
        )
        return r.json()[0]["translations"][0]["text"]
    else:
        raise ValueError(f"Unsupported translation provider: {provider}")
