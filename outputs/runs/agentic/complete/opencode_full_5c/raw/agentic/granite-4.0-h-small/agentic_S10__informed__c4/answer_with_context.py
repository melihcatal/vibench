import os
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose the LLM provider (must be defined via env vars per model_client)
PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")


async def answer_with_context(
    context: str, question: str, temperature: float = 0.0
) -> str:
    """Answer a natural‑language question using supplied context via the hosted LLM.
    Returns the concise answer as plain text.
    """
    config = get_provider_config(PROVIDER)
    client = get_llm_client(PROVIDER)

    request: PromptRequest = {
        "prompt": f"You are a helpful AI assistant. Given the context below, answer the question that follows. Keep the answer short and to the point.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:",
        "model": config.get("default_model", "claude-3-5-sonnet-20240620"),
        "temperature": temperature,
        "max_tokens": 256,
    }

    raw_resp = await client.chat_completions(request)
    normalized = normalize_response(raw_resp, PROVIDER)
    return normalized["text"]


# Provider‑specific async client definitions (same pattern as other files)
# def get_llm_client(provider: str) -> Any:
#     if provider == "anthropic":
#         import anthropic
#         return anthropic.AsyncClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
#     elif provider == "openai":
#         import openai
#         return openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     elif provider == "google":
#         from google.generativeai import generativeai
#         generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         return generativeai.get_model("gemini-1.5-pro-001").generate_content
#     elif provider == "bedrock":
#         import boto3
#         return boto3.client("bedrock-runtime", region_name="us-east-1")
#     elif provider == "watsonx":
#         from ibm_watsonx_ai.services import TextGeneration
#         return TextGeneration(api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID"))
#     elif provider == "dashscope":
#         import dashscope
#         return dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))

__all__ = ["answer_with_context"]
