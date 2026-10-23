import os
from typing import Any, Dict, List

# Example client wrappers for various providers (only one concrete provider is used in scored files)

PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Options: openai, google, bedrock, watsonx


class LLMClient:
    """Unified client interface for LLM inference.

    The concrete implementation selected by `PROVIDER` provides `chat` and `stream` methods.
    """

    def chat(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> Any:
        """Generate a single completion.")"
        raise NotImplementedError

    def stream(self, model: str, messages: List[Dict[str, Any]], **kwargs):
        """Yield streamed tokens/completions.")"
        raise NotImplementedError


if PROVIDER == "openai":
    import openai

    class _OpenAIClient(LLMClient):
        def __init__(self):
            openai.api_key = os.getenv("OPENAI_API_KEY")

        def chat(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            return openai.ChatCompletion.create(model=model, messages=messages, **kwargs)

        def stream(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            return openai.ChatCompletion.create(
                model=model, messages=messages, stream=True, **kwargs
            )

    LLMClient.chat = _OpenAIClient().chat
    LLMClient.stream = _OpenAIClient().stream

elif PROVIDER == "google":
    from google.generativeai import generate as genai

    class _GoogleClient(LLMClient):
        def chat(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            # Convert to genai format: system/user messages
            gen_messages = []
            for m in messages:
                gen_messages.append({"role": m["role"], "text": m["content"]})
            return genai.generate_content(
                model=model, messages=gen_messages, **kwargs
            )

        def stream(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            gen_messages = []
            for m in messages:
                gen_messages.append({"role": m["role"], "text": m["content"]})
            return genai.generate_stream(
                model=model, messages=gen_messages, **kwargs
            )

    LLMClient.chat = _GoogleClient().chat
    LLMClient.stream = _GoogleClient().stream

elif PROVIDER == "bedrock":
    import boto3
    from boto3.session import Session

    class _BedrockClient(LLMClient):
        def __init__(self):
            self.client = boto3.client(
                "bedrock-runtime",
                region_name=os.getenv("AWS_REGION"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )

        def chat(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            # Bedrock uses a different payload structure; we map locally
            payload = {
                "prompt": "\n\n".join(f"<{msg['role']}> {msg['content']}" for msg in messages),
                "modelId": model,
                "contentType": "application/json",
                "accept": "application/json",
                **kwargs,
            }
            response = self.client.invoke_model(body=payload)
            # Parse JSON response
            return response["body"].read()

        def stream(self, model: str, messages: List[Dict[str, Any]], **kwargs):
            # Bedrock streaming is handled via a separate API; stubbed here
            raise NotImplementedError

    LLMClient.chat = _BedrockClient().chat
    LLMClient.stream = _BedrockClient().stream

else:
    # Default to OpenAI implementation
    LLMClient.chat = LLMClient.chat_openai  # placeholder
    LLMClient.stream = LLMClient.stream_openai  # placeholder


def get_client() -> LLMClient:
    return LLMClient
