# [HELPER] model_models.py

from typing import Any, Dict, List, Optional


def normalize_chat_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert raw response from a hosted LLM into a uniform dictionary.

    Expected keys:
        - choices (list with at least one element)
        - choices[0].text or choices[0].message.content
    """
    choices = raw.get("choices", [])
    if not choices:
        raise ValueError("Response missing 'choices' field")
    choice = choices[0]
    # OpenAI style (text field) or Anthropic style (message.content)
    text: Optional[str] = None
    if "text" in choice:
        text = choice["text"]
    elif "message" in choice and "content" in choice["message"]:
        text = choice["message"]["content"]
    if text is None:
        raise ValueError("Choice does not contain extractable text")
    return {
        "text": text.strip(),
        "raw": raw,
    }


def normalize_embedding_response(raw: Any) -> List[float]:
    """Extract a flat list of floats from various embedding API responses."""
    # Example for OpenAI embeddings response
    if isinstance(raw, dict) and "data" in raw:
        vectors = raw["data"]
        if not vectors:
            raise ValueError("No vectors returned")
        # Assume first element's embedding list
        emb = vectors[0].get("embedding")
        if not emb or not isinstance(emb, list):
            raise ValueError("Embedding not found")
        return emb
    # Example for Gemini embeddings response (simplified)
    if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], list):
        return raw[0]
    raise ValueError("Unexpected embedding response format")
