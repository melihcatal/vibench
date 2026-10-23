from pydantic import BaseModel

class Payload(BaseModel):
    """Normalized request payload fields."""
    system: str = ""
    user: str = ""
    messages: list = []

    @property
    def as_dict(self) -> dict:
        # Flatten into a simple dict for downstream usage
        return {"system": self.system, "user": self.user, "messages": self.messages}

class Config(BaseModel):
    """Configuration block for model invocation."""
    provider: str = "anthropic"
    model_id: str = "claude-3-5-sonnet-20240620"
    deployment: str = "claude-3-5-sonnet-v1.0"
    deployment_id: str = ""
    api_key: str = ""  # e.g., ANTHROPIC_API_KEY or OPENAI_API_KEY

    class Config:
        env_prefix = "MODEL_"

class ModelRequest(BaseModel):
    """Single representation for requests across all scoring files."""
    payload: Payload = Payload()
    config: Config = Config()

    def dict(self, *, exclude_unset: bool = False, **kwargs) -> dict:
        return {
            "payload": self.payload.as_dict,
            "config": self.config.dict(exclude_unset=exclude_unset)
        }

class ModelResponse(BaseModel):
    """Normalized response structure used by all scoring files."""
    output: str = ""
    metadata: dict = {}

    @classmethod
    def from_raw(cls, raw: dict) -> "ModelResponse":
        # Subclasses can override to map provider‑specific keys
        return cls(output=raw.get("output", ""), metadata=raw.get("metadata", {}))
