import json
import urllib.request

from speech_client import load_config, openai_base_url


def embed_script(text: str):
    config = load_config()
    req = urllib.request.Request(
        f"{openai_base_url()}/embeddings",
        data=json.dumps({"model": "text-embedding-3-large", "input": text}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config.openai_api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")
