import os
import openai  # Azure OpenAI SDK (also works for Azure OpenAI endpoints)
from model_models import ModelInvocationResponse

# Configure Azure OpenAI client from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
if not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("AZURE_OPENAI_ENDPOINT not set")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
if not AZURE_OPENAI_API_KEY:
    raise RuntimeError("AZURE_OPENAI_API_KEY not set")

openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"  # adjust to latest version


class ManagedModelClient:
    """
    Thin wrapper around the Azure OpenAI SDK that encapsulates common
    request/response handling for Managed Model Platform workflows.
    """

    def invoke(
        self, deployment_id: str, messages: list, temperature: float = 0.0
    ) -> ModelInvocationResponse:
        resp = openai.ChatCompletion.create(
            deployment_id=deployment_id, messages=messages, temperature=temperature
        )
        return ModelInvocationResponse.from_sdk(resp)

    def stream_generate(
        self, deployment_id: str, messages: list, temperature: float = 0.0
    ):
        stream = openai.ChatCompletion.create(
            deployment_id=deployment_id,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        return stream

    def get_inference_profile_id(self) -> str:
        # Example helper – return a placeholder profile ID
        return "profile-abc123"
