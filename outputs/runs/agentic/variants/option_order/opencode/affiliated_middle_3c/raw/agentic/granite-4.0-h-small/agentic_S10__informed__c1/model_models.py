from typing import TypedDict, Any, Dict, List

# Normalization helpers – map each provider's raw response shape to a common schema
# This enables the same‑scenario code to stay provider‑agnostic downstream.


class Message(TypedDict):
    role: str
    content: str


class LLMResponse(TypedDict):
    choices: List[Dict[str, Any]]


class ProviderResponse(TypedDict):
    # Generic union – only the fields actually used by helpers need to exist
    # Real implementations fill in the exact keys per provider.
    pass


class NormalizedOutput(TypedDict):
    text: str
    json: Dict[str, Any] | None


class NormalizationHelpers:
    """Static utilities that translate a raw provider response into a canonical shape.
    \\n    At the moment only DashScope (Qwen) is implemented; other providers can be added
    with minimal boilerplate.
    """

    @staticmethod
    def from_dashscope(resp: ProviderResponse) -> NormalizedOutput:
        """Translate DashScope chat completions result to our NormalizedOutput."""
        # DashScope response format:
        # {
        #   "id": "...",
        #   "object": "chat.completion",
        #   "created": ...,
        #   "choices": [{
        #         "message": {"role": "assistant", "content": "..."},
        #         "finish_reason": "stop",
        #         "logprobs": None
        #   }]
        # }
        try:
            content = resp.choices[0]["message"]["content"]
            return NormalizedOutput(text=content, json=None)
        except (KeyError, TypeError):
            # If the model produced JSON output via a custom stop, attempt to parse
            import json

            try:
                json_obj = json.loads(content)
                return NormalizedOutput(text="", json=json_obj)
            except json.JSONDecodeError:
                return NormalizedOutput(text=content, json=None)

    @staticmethod
    def from_anthropic(resp: Any) -> NormalizedOutput:
        # Anthropic completions response format:
        # {
        #   "choices": [{"message": {"role": "assistant", "content": "..."}}]
        # }
        content = resp.choices[0]["message"]["content"]
        return NormalizedOutput(text=content, json=None)

    @staticmethod
    def from_mistral(resp: Any) -> NormalizedOutput:
        # Mistral chat response format is identical to Anthropic
        content = resp.choices[0]["message"]["content"]
        return NormalizedOutput(text=content, json=None)

    # Add more _from_ methods for other providers as needed
