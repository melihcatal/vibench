import os
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose the LLM provider (must exist as env vars as defined in model_client)
PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")


async def extract_json(text: str, schema: str, temperature: float = 0.0) -> dict:
    """Extract structured JSON conforming to `schema` from arbitrary text using the selected LLM.
    Returns a Python dict that matches the supplied JSON schema string.
    """
    config = get_provider_config(PROVIDER)
    client = get_llm_client(PROVIDER)

    request: PromptRequest = {
        "prompt": f"Extract data from the following text and return ONLY valid JSON that conforms to this JSON schema:\n\n{schema}\n\nText:\n{text}",
        "model": config.get("default_model", "gemini-1.5-pro-001"),
        "temperature": temperature,
        "max_tokens": 1024,
    }

    raw_resp = await client.chat_completions(request)
    normalized = normalize_response(raw_resp, PROVIDER)
    # Safely parse JSON; if parsing fails, raise a clear error
    import json

    try:
        return json.loads(normalized["text"])
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM output is not valid JSON: {normalized['text']}\n{exc}")


# Provider‑specific async client definitions (same pattern as in summarize_text)
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
#         return TextGeneration(api_key=os.getenv("WATSONX_API_KEY"),
#                               project_id=os.getenv("WATSONX_PROJECT_ID"))
#     elif provider == "dashscope":
#         import dashscope
#         return dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))

__all__ = ["extract_json"]
