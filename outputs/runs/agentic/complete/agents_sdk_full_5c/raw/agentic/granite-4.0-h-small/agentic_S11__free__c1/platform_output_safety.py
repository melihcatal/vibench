import json
from model_client import ManagedModelClient
from model_models import ModelRequest

def ensure_safe_output(text: str) -> str:
    """Simple content filter that strips disallowed elements (placeholder)."""
    # In production replace with provider moderation endpoint or custom ML filter
    safe = text.replace("<script>", "").replace("onload=", "").replace("javascript:", "")
    # Basic profanity filter (extensible)
    profanities = {"badword", "naughty"}
    for p in profanities:
        safe = safe.replace(p, "***")
    return safe

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are helpful.", "user": "Tell me a joke."},
                            config={"provider": "anthropic"})
    client = ManagedModelClient(provider=demo_req.config["provider"], api_key=os.getenv(demo_req.config["provider"] + "_API_KEY"))
    raw = client.chat(compute(demo_req.dict()))
    safe = ensure_safe_output(raw.get("output", ""))
    print(json.dumps({"text": safe, "metadata": raw.get("metadata")}, indent=2))
