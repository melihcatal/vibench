import urllib.request
import json

from speech_client import load_config, openai_base_url


def translate_script(text: str, target_language: str):
    config = load_config()
    req = urllib.request.Request(
        f"{openai_base_url()}/responses",
        data=json.dumps({"model": config.openai_model, "input": f"Translate to {target_language}: {text}"}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config.openai_api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")
