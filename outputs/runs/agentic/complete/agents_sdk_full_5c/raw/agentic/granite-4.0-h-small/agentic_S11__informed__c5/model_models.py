# model_models.py
# Managed Model Platform Workflow: request, response, and normalization helpers
# Provider: Azure OpenAI
from typing import Any, Dict, List

# Request structure for Azure OpenAI chat completion
ChatRequest = Dict[str, Any]

# Response structure after invoking Azure OpenAI
ChatResponse = Dict[str, Any]

# Normalized output shape used downstream in workflow
NormalizedOutput = Dict[str, Any]

ResponseUsage = Dict[str, int]


def build_chat_request(user_prompt: str, **kwargs: Any) -> ChatRequest:
    """Construct a provider‑specific chat request payload."""
    payload: ChatRequest = {
        "model": kwargs.get("deployment", os.getenv("AZURE_OPENAI_DEPLOYMENT")),
        "messages": [{"role": "user", "content": user_prompt}],
    }
    # Pass additional generation options (max_tokens, temperature, etc.)
    for key in ["max_tokens", "temperature", "top_p", "frequency_penalty", "presence_penalty"]:
        if kwargs.get(key) is not None:
            payload[key] = kwargs[key]
    return payload


def parse_chat_response(raw_response: ChatResponse) -> NormalizedOutput:
    """Extract useful fields from raw Azure OpenAI response."""
    output_content = raw_response.get("choices", [{}])[0].get("message", {}).get("content", "")
    usage: ResponseUsage = raw_response.get("usage", {})
    return {
        "text": output_content,
        "usage": {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "model": usage.get("model"),
        },
    }

if __name__ == "__main__":
    # Quick demo of building and parsing a request/response
    demo_prompt = "Hello, world!"
    req = build_chat_request(demo_prompt, deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), max_tokens=64)
    # Raw response simulation (replace with real call in production)
    raw_resp = {
        "choices": [{"message": {"content": "I responded."}}],
        "usage": {"prompt_tokens": 6, "completion_tokens": 3, "total_tokens": 9, "model": "gpt-35-turbo"},
    }
    print(parse_chat_response(raw_resp))
