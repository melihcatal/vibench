import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class ManagedModelClient(ABC):
    """Abstract base client for any managed model platform."""
    
    @classmethod
    @abstractmethod
    def from_env(cls) -> "ManagedModelClient":
        """Instantiate a client using environment variables or other local config."""
        pass
    
    @abstractmethod
def invoke(self, request: Dict[str, Any]) -> Any:
    """Synchronous invocation returning provider‑specific response object."""
        pass
    
    @abstractmethod
    async def invoke_stream(self, request: Dict[str, Any]) -> AsyncIterator[Any]:
    """Async streaming invocation yielding response chunks."""
        pass

# ---------------------------------------------------------------------------
# Example concrete implementations using a real provider (Amazon Bedrock)
# ---------------------------------------------------------------------------
# Uncomment the implementation below if you want to use Bedrock as the concrete provider.

# from boto3 import client as boto3_client
# from botocore.client import Config as BotoConfig
#
# class BedrockClient(ManagedModelClient):
#     _boto_client: Optional[any] = None
# 
#     @classmethod
#     def from_env(cls) -> "BedrockClient":
#         """Create client using AWS credentials from env (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)."""
#         boto_cfg = BotoConfig(
#             region_name=os.getenv("AWS_REGION", "us-east-1")
#         )
#         cls._boto_client = boto3_client(
#             "bedrock-runtime",
#             config=boto_cfg,
#         )
#         return cls()
#     
#     def invoke(self, request: Dict[str, Any]) -> any:
#         payload = {
#             "inputs": request["prompt"],
#             "deploymentId": request["deployment"]
#         }
#         response = self._boto_client.invoke_model(
#             contentType="application/json",
#             deploymentId=payload["deploymentId"],
#             body=json.dumps(payload["inputs"])
#         )
#         return response  # response is a botocore response object
#     
#     async def invoke_stream(self, request: Dict[str, Any]) -> AsyncIterator[Any]:
#         # Bedrock currently returns a single chunk; for true streaming use other providers.
#         yield self.invoke(request)

# ---------------------------------------------------------------------------
# The above concrete client can be swapped with any other provider (Vertex AI,
# Hugging Face, Azure OpenAI, etc.) by providing a matching implementation of
# ManagedModelClient. The rest of the workflow code remains unchanged.
# ---------------------------------------------------------------------------
