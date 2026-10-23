from typing import TypedDict, List, Any

class PromptRequest(TypedDict):
    """Request payload for model inference – include user prompt and optional parameters."""
    prompt: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 256
    stop: List[str] = None

class InferenceResponse(TypedDict):
    """Raw response from the hosted LLM service."""
    model: str
    usage: Any
    content: List[Dict[str, Any]]

class NormalizedResponse(TypedDict):
    """Unified response shape used by the integration files."""
    text: str
    usage: Any
    model: str

# Example helper to build a payload for a given provider
def build_payload(provider: str, request: PromptRequest) -> Dict[str, Any]:
    """Translate our internal PromptRequest into provider‑specific payload."""
    payload: Dict[str, Any] = {}
    if provider == "anthropic":
        payload["model"] = "claude-3-5-sonnet-20240620"
        payload["messages"] = [dict(role="user", content=request["prompt"])])
        # optional fields can be added here
    elif provider == "openai":
        payload["model"] = request["model"]
        payload["messages"] = [dict(role="user", content=request["prompt"])])
        payload["temperature"] = request["temperature"]
        payload["max_tokens"] = request["max_tokens"]
        if request["stop"]:
            payload["stop"] = request["stop"]
    elif provider == "google":
        payload["candidateCount"] = 1
        prompt = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": request["prompt"]}],
                }
            ],
        }
        payload["generationConfig"] = {
            "temperature": request["temperature"],
            "maxOutputTokens": request["max_tokens"],
        }
        payload["instances"] = [{"input": prompt}]
    elif provider == "bedrock":
        payload["modelId"] = request["model"]
        prompt = {
            "parts": [
                {
                    "text": request["prompt"]
                }
            ]
        }
        payload["input"] = {
            "prompt": prompt,
            "contentType": "text/plain"
        }
        payload["maxTokens"] = request["max_tokens"]
        payload["temperature"] = request["temperature"]
    elif provider == "watsonx":
        payload["prompt"] = request["prompt"]
        payload["modelId"] = request["model"]
        payload["temperature"] = request["temperature"]
        payload["max_tokens"] = request["max_tokens"]
        if request["stop"]:
            payload["stopSequences"] = request["stop"]
    elif provider == "dashscope":
        payload["model"] = request["model"]
        payload["messages"] = [dict(role="user", content=request["prompt"])])
        payload["temperature"] = request["temperature"]
        payload["max_tokens"] = request["max_tokens"]
        if request["stop"]:
            payload["stop"] = request["stop"]
    else:
        raise ValueError(f"Unsupported provider for payload build: {provider}")
    return payload

# Example helper to extract fields from a raw response
def extract_fields(raw_resp: Dict[str, Any], provider: str) -> NormalizedResponse:
    """Convert raw service response to NormalizedResponse shape."""
    if provider == "anthropic":
        return {
            "text": raw_resp.get("content", [{}])[0].get("text"),
            "usage": raw_resp.get("usage"),
            "model": raw_resp.get("model"),
        }
    elif provider == "openai":
        return {
            "text": raw_resp.get("choices", [{}])[0].get("message", {}).get("content"),
            "usage": raw_resp.get("usage"),
            "model": raw_resp.get("model"),
        }
    elif provider == "google":
        cand = raw_resp.get("candidates", [{}])[0]
        return {
            "text": cand.get("content", {}).get("parts", [{}])[0].get("text"),
            "usage": None,
            "model": "gemini-1.5-pro-001",
        }
    elif provider == "bedrock":
        body = raw_resp.get("body", {})
        return {
            "text": body.get("contentItems", [{}])[0].get("text"),
            "usage": None,
            "model": "nova-2024-04",
        }
    elif provider == "watsonx":
        return {
            "text": raw_resp.get("result", {}).get("output", {}).get("text"),
            "usage": None,
            "model": raw_resp.get("model"),
        }
    elif provider == "dashscope":
        choice = raw_resp.get("choice", [{}])[0]
        return {
            "text": choice.get("message", {}).get("content"),
            "usage": None,
            "model": raw_resp.get("model"),
        }
    raise ValueError(f"No extractor for provider: {provider}")
