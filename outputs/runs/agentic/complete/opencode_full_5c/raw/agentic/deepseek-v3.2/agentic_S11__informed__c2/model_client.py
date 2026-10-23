import os
import boto3
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class BedrockConfig:
    region: str = "us-east-1"
    model_id: str = "anthropic.claude-v2"
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 0.9

    @classmethod
    def from_env(cls) -> "BedrockConfig":
        return cls(
            region=os.getenv("AWS_REGION", "us-east-1"),
            model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2"),
            max_tokens=int(os.getenv("BEDROCK_MAX_TOKENS", "100")),
            temperature=float(os.getenv("BEDROCK_TEMPERATURE", "0.7")),
            top_p=float(os.getenv("BEDROCK_TOP_P", "0.9")),
        )


class BedrockClient:
    def __init__(self, config: Optional[BedrockConfig] = None):
        self.config = config or BedrockConfig.from_env()
        self._runtime_client = None
        self._bedrock_client = None

    @property
    def runtime_client(self):
        if self._runtime_client is None:
            self._runtime_client = boto3.client(
                service_name="bedrock-runtime", region_name=self.config.region
            )
        return self._runtime_client

    @property
    def bedrock_client(self):
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client(
                service_name="bedrock", region_name=self.config.region
            )
        return self._bedrock_client

    def get_default_model_id(self) -> str:
        return self.config.model_id

    def validate_credentials(self) -> bool:
        try:
            sts = boto3.client("sts", region_name=self.config.region)
            sts.get_caller_identity()
            return True
        except Exception:
            return False

    def create_request_body(self, prompt: str, **kwargs) -> Dict[str, Any]:
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        temperature = kwargs.get("temperature", self.config.temperature)
        top_p = kwargs.get("top_p", self.config.top_p)

        return {
            "prompt": prompt,
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop_sequences": ["\n\nHuman:"],
        }
