import os
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose the LLM provider (must exist as env vars as defined in model_client)
PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")


async def summarize_text(
    text: str, max_tokens: int = 512, temperature: float = 0.7
) -> str:
    """Summarize long input text using the selected hosted LLM.
    Returns the concise summary as plain text.
    """
    config = get_provider_config(PROVIDER)
    client = get_llm_client(
        PROVIDER
    )  # concrete client will be imported in provider specific module

    request: PromptRequest = {
        "prompt": f"Summarize the following text in 3-4 sentences, preserving the main ideas:\n\n{text}",
        "model": config.get("default_model", "claude-3-5-sonnet-20240620"),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    raw_resp = await client.chat_completions(request)
    normalized = normalize_response(raw_resp, PROVIDER)
    return normalized["text"]


# -- Provider‑specific client stubs -------------------------------------------------
# Each provider must implement its own async `chat_completions` function that receives
# a PromptRequest dict and returns the raw JSON response from the hosted API.
# The implementations can use SDKs, HTTP calls, or REST clients as appropriate.

# Example: Anthropic (Messages API) – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "anthropic":
#         import anthropic
#         client = anthropic.AsyncClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
#         return client

# Example: OpenAI (Chat Completion) – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "openai":
#         import openai
#         client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         return client

# Example: Google Gemini API – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "google":
#         from google.generativeai import generativeai
#         generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         model = generativeai.get_model("gemini-1.5-pro-001")
#         return model.generate_content

# Example: Amazon Bedrock – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "bedrock":
#         import boto3
#         client = boto3.client("bedrock-runtime", region_name="us-east-1")
#         return client

# Example: watsonx – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "watsonx":
#         from ibm_watsonx_ai.services import TextChatGeneration
#         client = TextChatGeneration(api_key=os.getenv("WATSONX_API_KEY"),
#                                     project_id=os.getenv("WATSONX_PROJECT_ID"))
#         return client.chat_completion

# Example: DashScope – hypothetical async function
# def get_llm_client(provider: str):
#     if provider == "dashscope":
#         import dashscope
#         client = dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
#         return client.chat_completion

# If the provider’s SDK supports async, wrap the call with `await`. If the SDK is
# synchronous, you can run it in an executor or simply prefix the call with `await` in
# the adapter layer.

# ---------------------------------------------------------------------------

__all__ = ["summarize_text"]
