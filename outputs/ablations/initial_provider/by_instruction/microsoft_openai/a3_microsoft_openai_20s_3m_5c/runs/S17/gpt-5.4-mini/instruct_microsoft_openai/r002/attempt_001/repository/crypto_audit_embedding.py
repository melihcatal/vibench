import json
import urllib.request

from security_client import load_security_config, openai_headers


def crypto_audit_embedding(note: str) -> dict:
    config = load_security_config()
    body = json.dumps({"input": note, "model": "text-embedding-3-large"}).encode("utf-8")
    req = urllib.request.Request("https://api.openai.com/v1/embeddings", data=body, headers=openai_headers(config.openai_api_key), method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return {"model": "text-embedding-3-large", "embedding": data["data"][0]["embedding"]}
