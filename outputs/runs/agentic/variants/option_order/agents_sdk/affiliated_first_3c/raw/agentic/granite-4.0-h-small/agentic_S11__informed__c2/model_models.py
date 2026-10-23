from typing import NamedTuple, Any, Dict


class PromptRequest(NamedTuple):
    """Local representation of the request payload for the managed model."""
    inputs: str
    parameters: Dict[str, Any] = None


class PromptResponse(NamedTuple):
    """Local normalized response container that includes provider metadata."""
    generated_text: str
    provider: str
    request_id: Optional[str] = None
    model_id: Optional[str] = None
    usage_info: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None

    def raw_json(self) -> str:
        """Return a JSON string representation of raw provider payload."""
        return json.dumps(self.raw, indent=2) if self.raw else "{}"