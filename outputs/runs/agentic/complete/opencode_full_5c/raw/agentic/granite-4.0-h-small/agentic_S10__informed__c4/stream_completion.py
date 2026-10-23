import os
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose the LLM provider (must be set as env var LLM_PROVIDER)
PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")


async def stream_completion(
    prompt: str, max_tokens: int = 256, temperature: float = 0.7
) -> None:
    """Stream partial token output from the LLM as it is generated.
    Yields each partial string fragment received from the provider.
    """
    config = get_provider_config(PROVIDER)
    client = get_llm_client(PROVIDER)

    request: PromptRequest = {
        "prompt": prompt,
        "model": config.get("default_model", "gemini-1.5-pro-001"),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    await client.stream_chat_completions(request, yield_handler=_yield_handler)


async def _yield_handler(chunk: dict):
    # The concrete shape depends on the provider, so we normalize minimally here
    # Only return the raw text fragment; callers can decide how to stitch them together
    if "text" in chunk:
        yield chunk["text"]
    elif "content" in chunk:
        # Anthropic style
        yield chunk["content"]
    elif "response" in chunk:
        # OpenAI style chunk object
        yield chunk["response"]["content"]
    else:
        raise ValueError("Unknown streaming chunk format: " + str(chunk))


# Provider‑specific async streaming client definitions
# def get_llm_client(provider: str) -> Any:
#     if provider == "anthropic":
#         import anthropic
#         client = anthropic.AsyncClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
#         return client.stream_chat_messages
#     elif provider == "openai":
#         import openai
#         client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         return client.stream_chat_completions
#     elif provider == "google":
#         from google.generativeai import generativeai
#         generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         model = generativeai.get_model("gemini-1.5-pro-001")
#         # Google Gemini currently does not expose a true token‑by‑token stream via SDK; you may need to
#         # fall back to manual async HTTP polling if streaming is required
#     elif provider == "bedrock":
#         import boto3
#         client = boto3.client("bedrock-runtime", region_name="us-east-1")
#         # Bedrock supports streaming via `InvokeModelWithResponseStream`
#         return client
#     elif provider == "watsonx":
#         from ibm_watsonx_ai.services import TextGeneration
#         client = TextGeneration(api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID"))
#         # Watsonx returns streamed data via async iterator; return client.chat_completion_stream
#         return client.chat_completion_stream
#     elif provider == "dashscope":
#         import dashscope
#         client = dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
#         return client.chat_completion_stream

__all__ = ["stream_completion"]
