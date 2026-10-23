import json
from model_client import ManagedModelClient
from model_models import ModelRequest

def collect_metadata(request: ModelRequest, raw_response):
    """Extract platform-specific metadata (usage, model handle, etc.) alongside the model output."""
    provider = request.config.get("provider", "anthropic")
    if provider == "anthropic":
        # Example metadata fields from Anthropic
        usage = raw_response.get("usage", {})
        model_handle = raw_response.get("model", "claude-3-5-sonnet-20240620")
        return {
            "output": raw_response.get("content", [{}])[0].get("text", ""),
            "metadata": {
                "model_id": model_handle,
                "usage": usage,
                "request_id": raw_response.get("id", "")
            }
        }
    elif provider == "openai":
        # Example metadata fields from OpenAI
        usage = raw_response.get("usage", {})
        model_handle = raw_response.get("model", "gpt-4o-mini")
        return {
            "output": raw_response.get("choices", [{}])[0].get("message", {}).get("content", ""),
            "metadata": {
                "model_id": model_handle,
                "usage": usage,
                "request_id": raw_response.get("id", "")
            }
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are brief.", "user": "Summarize quantum computing in 20 words."},
                            config={"provider": "anthropic"})
    client = ManagedModelClient(provider=demo_req.config["provider"], api_key=os.getenv(demo_req.config["provider"] + "_API_KEY"))
    raw = client.chat(compute(demo_req.dict()))
    result = collect_metadata(demo_req, raw)
    print(json.dumps(result, indent=2))
