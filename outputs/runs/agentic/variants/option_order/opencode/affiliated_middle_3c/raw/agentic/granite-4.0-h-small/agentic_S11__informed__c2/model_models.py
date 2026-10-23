# Helper module: Model Metadata
class InferenceRequest(TypedDict):
    """Request payload for model inference."""

    prompt: str
    temperature: float | None
    max_tokens: int | None


class InferenceResponse(TypedDict):
    """Response from model inference (generic wrapper)."""

    text: str
    raw: dict  # provider-specific raw payload


# Example of normalising a response from a provider into a unified format
from model_client import ManagedModelClient


def normalize_response(provider: str, raw_response: dict) -> InferenceResponse:
    """Convert provider-specific response into a consistent InferenceResponse."""
    if provider == "huggingface":
        # Hugging Face returns a dict with 'generated_text'
        return {"text": raw_response.get("generated_text", ""), "raw": raw_response}
    elif provider == "bedrock":
        # AWS Bedrock returns a large JSON with 'body' attribute
        return {
            "text": raw_response.get("body", {}).get("text", ""),
            "raw": raw_response,
        }
    elif provider == "watsonx":
        # Watsonx returns a dict with 'generated_text'
        return {"text": raw_response.get("generated_text", ""), "raw": raw_response}
    elif provider == "vertex":
        # Vertex AI returns a structured dict with 'content'
        return {"text": raw_response.get("content", ""), "raw": raw_response}
    elif provider == "alibaba":
        # DashScope returns a dict with 'result' that contains generated text
        return {"text": raw_response.get("result", ""), "raw": raw_response}
    elif provider == "azure":
        # Azure OpenAI returns a dict with 'choices' that include 'message'
        return {
            "text": raw_response.get("choices")[0]
            .get("message", {})
            .get("content", ""),
            "raw": raw_response,
        }
    else:
        raise ValueError(f"Unsupported provider for normalization: {provider}")


# Helper to extract metadata like usage, request ID, etc.
from model_client import ManagedModelClient


def extract_metadata(provider: str, raw_response: dict) -> dict:
    if provider == "huggingface":
        return {
            "request_id": raw_response.get("request_id"),
            "usage": raw_response.get("usage"),
        }
    elif provider == "bedrock":
        return {
            "request_id": raw_response.get("requestId"),
            "usage": {"characters": raw_response.get("charactersGenerated", 0)},
        }
    elif provider == "watsonx":
        return {
            "request_id": raw_response.get("id"),
            "usage": raw_response.get("usage"),
        }
    elif provider == "vertex":
        return {
            "request_id": raw_response.get("name"),
            "usage": raw_response.get("usage"),
        }
    elif provider == "alibaba":
        return {
            "request_id": raw_response.get("id"),
            "usage": raw_response.get("usage"),
        }
    elif provider == "azure":
        return {
            "request_id": raw_response.get("id"),
            "usage": raw_response.get("usage"),
        }
    else:
        raise ValueError(f"Unsupported provider for metadata: {provider}")


# Usage example (would be called inside higher‑level files)
if __name__ == "__main__":
    config = {
        "provider": "huggingface",
        "model_id": "your-model-id",
        "hf_token": os.getenv("HF_TOKEN"),
    }
    client = ManagedModelClient(config)
    raw = client.invoke({"prompt": "Hello world"})
    response = normalize_response(config["provider"], raw)
    meta = extract_metadata(config["provider"], raw)
    print("Response:", response)
    print("Metadata:", meta)
