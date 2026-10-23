import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class BedrockConfig:
    """Configuration for Amazon Bedrock client."""

    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    region: str = "us-east-1"
    default_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout: int = 30

    def __post_init__(self):
        """Load from environment variables if not provided."""
        if not self.aws_access_key_id:
            self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if not self.aws_secret_access_key:
            self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not self.region:
            self.region = os.getenv("AWS_REGION", "us-east-1")


class BedrockClient:
    """Client helper for Amazon Bedrock operations."""

    def __init__(self, config: Optional[BedrockConfig] = None):
        self.config = config or BedrockConfig()
        self._runtime_client = None
        self._bedrock_client = None

    @property
    def runtime_client(self):
        """Lazy initialization of Bedrock Runtime client."""
        if self._runtime_client is None:
            import boto3

            self._runtime_client = boto3.client(
                "bedrock-runtime",
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key,
                region_name=self.config.region,
            )
        return self._runtime_client

    @property
    def bedrock_client(self):
        """Lazy initialization of Bedrock client."""
        if self._bedrock_client is None:
            import boto3

            self._bedrock_client = boto3.client(
                "bedrock",
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key,
                region_name=self.config.region,
            )
        return self._bedrock_client

    def validate_credentials(self) -> bool:
        """Validate AWS credentials by attempting to list models."""
        try:
            response = self.bedrock_client.list_foundation_models(maxResults=1)
            return "modelSummaries" in response
        except Exception:
            return False

    def get_available_models(self, max_results: int = 100) -> list:
        """Get list of available foundation models."""
        try:
            response = self.bedrock_client.list_foundation_models(
                maxResults=max_results
            )
            return response.get("modelSummaries", [])
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def get_model_details(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model."""
        try:
            response = self.bedrock_client.get_foundation_model(
                modelIdentifier=model_id
            )
            return response.get("modelDetails")
        except Exception as e:
            print(f"Error getting model details: {e}")
            return None

    def format_request_body(self, model_id: str, prompt: str, **kwargs) -> str:
        """Format request body according to model provider specifications."""
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        temperature = kwargs.get("temperature", self.config.temperature)

        if "anthropic" in model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            if kwargs.get("system"):
                body["system"] = kwargs["system"]
            if kwargs.get("stream"):
                body["stream"] = True
        elif "meta" in model_id:
            body = {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": temperature,
            }
            if kwargs.get("stream"):
                body["stream"] = True
        elif "amazon" in model_id:
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                },
            }
        else:
            body = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            if kwargs.get("stream"):
                body["stream"] = True

        return json.dumps(body)

    def parse_response(
        self, model_id: str, response_body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse response based on model provider."""
        if "anthropic" in model_id:
            return {
                "text": response_body["content"][0]["text"],
                "usage": response_body.get("usage", {}),
                "stop_reason": response_body.get("stop_reason"),
                "model_id": model_id,
            }
        elif "meta" in model_id:
            return {
                "text": response_body["generation"],
                "prompt_token_count": response_body.get("prompt_token_count"),
                "generation_token_count": response_body.get("generation_token_count"),
                "stop_reason": response_body.get("stop_reason"),
                "model_id": model_id,
            }
        elif "amazon" in model_id:
            return {
                "text": response_body["results"][0]["outputText"],
                "input_token_count": response_body.get("inputTextTokenCount"),
                "results": response_body.get("results", []),
                "model_id": model_id,
            }
        else:
            return {
                "text": response_body.get(
                    "completion", response_body.get("generated_text", "")
                ),
                "response_body": response_body,
                "model_id": model_id,
            }
