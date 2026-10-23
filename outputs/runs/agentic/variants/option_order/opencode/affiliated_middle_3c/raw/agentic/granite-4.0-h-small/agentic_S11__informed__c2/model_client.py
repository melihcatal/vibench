# Helper module: ManagedModelClient
import os
from typing import TypedDict


class PlatformConfig(TypedDict):
    provider: str
    model_id: str | None
    deployment_id: str | None
    inference_profile_id: str | None


def load_config() -> PlatformConfig:
    """Load configuration from environment variables specific to the selected provider."""
    provider = os.getenv("PROVIDER", "huggingface")
    if provider == "huggingface":
        # Hugging Face inference API token is required
        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError("HF_TOKEN environment variable not set")
        return {
            "provider": "huggingface",
            "model_id": os.getenv("HF_MODEL_ID"),
            "deployment_id": None,
            "inference_profile_id": None,
        }
    elif provider == "bedrock":
        # AWS credentials are required
        aws_access = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not aws_access or not aws_secret:
            raise RuntimeError("AWS credentials not set")
        return {
            "provider": "bedrock",
            "model_id": os.getenv("BEDROCK_MODEL_ID"),
            "deployment_id": None,
            "inference_profile_id": None,
        }
    elif provider == "watsonx":
        # Watsonx requires API key and project ID
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        if not api_key or not project_id:
            raise RuntimeError("WATSONX credentials not set")
        return {
            "provider": "watsonx",
            "model_id": os.getenv("WATSONX_MODEL_ID"),
            "deployment_id": None,
            "inference_profile_id": None,
        }
    elif provider == "vertex":
        # Vertex AI service account credentials
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_path:
            raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not set")
        return {
            "provider": "vertex",
            "model_id": os.getenv("VERTEX_MODEL_ID"),
            "deployment_id": None,
            "inference_profile_id": None,
        }
    elif provider == "alibaba":
        # Alibaba Cloud access key pair
        access_key = os.getenv("ALIBABA_ACCESS_KEY_ID")
        secret_key = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
        if not access_key or not secret_key:
            raise RuntimeError("Alibaba credentials not set")
        return {
            "provider": "alibaba",
            "model_id": os.getenv("ALIBABA_MODEL_ID"),
            "deployment_id": None,
            "inference_profile_id": None,
        }
    elif provider == "azure":
        # Azure OpenAI endpoint and key
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        key = os.getenv("AZURE_OPENAI_API_KEY")
        if not endpoint or not key:
            raise RuntimeError("Azure OpenAI credentials not set")
        return {
            "provider": "azure",
            "model_id": os.getenv("AZURE_MODEL_ID"),
            "deployment_id": os.getenv("AZURE_DEPLOYMENT_ID"),
            "inference_profile_id": None,
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")


class ManagedModelClient:
    """Generic client wrapper to abstract provider-specific model invocation.","""

    def __init__(self, config: PlatformConfig):
        self.config = config
        self.provider = config["provider"]
        # Additional provider-specific client initialization can be added here.

    def invoke(self, request: dict) -> dict:
        """Invoke the underlying provider. Placeholder implementation.","""
        if self.provider == "huggingface":
            from huggingface_hub import InferenceApi

            api = InferenceApi(
                repo_id=self.config["model_id"], token=os.getenv("HF_TOKEN")
            )
            result = api.pipe(request["prompt"]).__next__()  # first chunk
            return result
        elif self.provider == "bedrock":
            import boto3

            bedrock = boto3.client(
                service_name="bedrock-runtime",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
            resp = bedrock.post_generation_prompt(
                Prompt=request["prompt"], MaxToken=256
            )
            return resp
        elif self.provider == "watsonx":
            from ibm_watsonx_ai import Client

            client = Client(
                apikey=os.getenv("WATSONX_API_KEY"),
                project_id=os.getenv("WATSONX_PROJECT_ID"),
            )
            inference = client.ai_runtime.InferenceJob.from_prompt(
                request["prompt"], model_id=self.config["model_id"]
            )
            return inference.result
        elif self.provider == "vertex":
            # Placeholder: Vertex AI generative AI SDK instantiation
            from vertexai.preview.language_models import ChatModel

            model = ChatModel.from_pretrained("gemini-pro")
            response = model.predict(request["prompt"])
            return response.dict()
        elif self.provider == "alibaba":
            from dashscope import TextGenerationClient

            client = TextGenerationClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
            result = client.generate(
                request["prompt"], model_id=self.config["model_id"]
            )
            return result
        elif self.provider == "azure":
            # Placeholder for Azure OpenAI deployment
            return {"placeholder": "azure-response"}
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_model_id(self) -> str:
        """Return the configured model identifier.","""
        return self.config["model_id"]

    def get_deployment_id(self) -> str | None:
        """Return deployment identifier, if any.","""
        return self.config.get("deployment_id")

    def get_inference_profile_id(self) -> str | None:
        """Return inference profile identifier, if any.","""
        return self.config.get("inference_profile_id")
