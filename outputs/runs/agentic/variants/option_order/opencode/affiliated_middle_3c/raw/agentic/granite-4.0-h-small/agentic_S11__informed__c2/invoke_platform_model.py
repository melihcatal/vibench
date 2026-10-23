import os
from model_client import ManagedModelClient
from model_models import InferenceRequest, InferenceResponse
from collect_platform_metadata import collect_metadata
from select_platform_resource import select_provider
from stream_platform_generation import stream_generation


class PlatformModelInference:
    """Facade to manage platform model inference with provider selection, invocation, streaming, and metadata collection."""

    def __init__(self, config: dict):
        self.config = config
        self.client = ManagedModelClient(config)
        self.provider = config.get("provider")
        self.model_id = select_provider("model", self.config)
        self.deployment_id = select_provider("deployment", self.config)
        self.inference_profile_id = select_provider("inference_profile", self.config)
        # Ensure provider-specific env vars are present
        if self.provider == "huggingface":
            os.getenv("HF_TOKEN")
        elif self.provider == "bedrock":
            os.getenv("AWS_ACCESS_KEY_ID")
            os.getenv("AWS_SECRET_ACCESS_KEY")
        elif self.provider == "watsonx":
            os.getenv("WATSONX_API_KEY")
            os.getenv("WATSONX_PROJECT_ID")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def invoke(self, request: InferenceRequest) -> InferenceResponse:
        """Synchronously invoke the model and return a single response."""
        if self.provider == "huggingface":
            from huggingface_hub import InferenceApi

            api = InferenceApi(repo_id=self.model_id, token=os.getenv("HF_TOKEN"))
            response = api.pipe(request["prompt"])  # returns a generator
            # Take first chunk as final output
            chunk = next(response)
            return InferenceResponse(text=chunk.get("generated_text", ""), raw=chunk)
        elif self.provider == "bedrock":
            import boto3

            bedrock = boto3.client(
                service_name="bedrock-runtime",
                region_name=self.config.get("region", "us-east-1"),
            )
            resp = bedrock.post_generation_prompt(
                Prompt=request["prompt"], MaxToken=request.get("max_tokens", 256)
            )
            text = resp.get("body").read().decode()
            return InferenceResponse(text=text, raw=resp)
        elif self.provider == "watsonx":
            from ibm_watsonx_ai import Client

            client_wx = Client(
                apikey=os.getenv("WATSONX_API_KEY"),
                project_id=os.getenv("WATSONX_PROJECT_ID"),
            )
            inference_api = client_wx.ai_runtime.InferenceJob.from_prompt(
                request["prompt"], model_id=self.model_id
            )
            # Assume one-shot response
            result = inference_api.result
            return InferenceResponse(text=result.get("generated_text", ""), raw=result)
        else:
            raise ValueError(f"Unsupported provider for invoke: {self.provider}")

    def stream(self, request: InferenceRequest) -> tuple[list[InferenceResponse], dict]:
        """Stream generation and collect metadata together."""
        responses, meta = stream_generation(
            self.provider, request["prompt"], self.config
        )
        metadata = collect_metadata(self.provider, responses, self.config)
        return responses, metadata

    def select_resource(self, resource_type: str) -> str:
        """Select a platform resource such as model, deployment, or inference profile."""
        return select_provider(resource_type, self.config)
