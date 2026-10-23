import requests

from document_client import get_deepl_config


def ocr_translate(text: str, target_lang: str = "EN") -> str:
    cfg = get_deepl_config()
    response = requests.post(
        f"{cfg['base_url']}/v2/translate",
        data={"auth_key": cfg["auth_key"], "text": text, "target_lang": target_lang},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]
