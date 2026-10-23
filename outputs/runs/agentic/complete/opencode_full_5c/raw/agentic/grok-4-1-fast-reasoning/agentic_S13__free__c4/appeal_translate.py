import requests
from urllib.parse import urlencode
from safety_client import get_api_key


def appeal_translate(text: str, target_lang: str = "EN") -> str:
    api_key = get_api_key("DEEPL_AUTH_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    params = {"auth_key": api_key, "text": text, "target_lang": target_lang}
    response = requests.post(url, data=urlencode(params))
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
