import os
import json
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose a safety model (must be set via env var SAFETY_MODEL, e.g. "tisane")
SAFETY_MODEL = os.getenv("SAFETY_MODEL", "tisane")


async def is_prompts_safe(prompt: str) -> bool:
    """Check the provided user prompt for unsafe or policy‑violating content.
    Returns True if the prompt passes moderation, False otherwise.
    """
    config = get_provider_config(SAFETY_MODEL)
    client = get_safety_client(SAFETY_MODEL)

    # Build a request that matches the safety service's expected format.
    # Most services accept a plain text string; Tisane also accepts a JSON payload.
    request = {
        "text": prompt,
    }

    raw_resp = await client.moderate_text(request)
    # Normalization not required for safety – we directly inspect the response fields.
    if SAFETY_MODEL == "tisane":
        # Tisane returns a dict with keys like 'results' containing categories
        violations = raw_resp.get("results", [])
        unsafe = any(v.get("severity", "safe") != "safe" for v in violations)
        return not unsafe
    elif SAFETY_MODEL == "watsonx":
        # watsonx guardrails returns {'violations': [{...}]} or empty list
        vio = raw_resp.get("violations", [])
        return len(vio) == 0
    elif SAFETY_MODEL == "azure":
        # Azure Content Safety returns {'classification': {...}} with scores
        classification = raw_resp.get("classification", {})
        # Consider a score >= 0.8 as blocked (example rule)
        return classification.get("score", 0.0) < 0.8
    elif SAFETY_MODEL == "aws":
        # Amazon Comprehend Toxicity returns {'toxicity': float}
        score = raw_resp.get("toxicity", 0.0)
        return score < 0.5
    elif SAFETY_MODEL == "alibaba":
        # Alibaba returns {'safety': {'label': 'safe'/ 'unsafe'}}
        label = raw_resp.get("safety", {}).get("label")
        return label == "safe"
    raise ValueError(f"Unsupported safety provider: {SAFETY_MODEL}")


async def is_generated_safe(text: str) -> bool:
    """Re‑evaluate model output for policy violations after generation.
    Same return semantics as is_prompts_safe.
    """
    return await is_prompts_safe(text)


# Provider‑specific async safety client definitions
# def get_safety_client(provider: str) -> Any:
#     if provider == "tisane":
#         import requests
#         return lambda req: requests.post(
#             "https://api.tisane.ai/moderate",
#             headers={"Authorization": f"Bearer {os.getenv('TISANE_API_KEY')}",
#                      "Content-Type": "application/json"},
#             json=req).json()
#     elif provider == "watsonx":
#         from ibm_watsonx_ai import APIClient
#         client = APIClient()
#         return client.guardrails.check_text
#     elif provider == "azure":
#         from azure.ai.contentsafety import ContentSafetyClient, ModerationOptions
#         return ContentSafetyClient(endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
#                                    credential=azure.core.SecretValue(os.getenv("AZURE_CONTENT_SAFETY_KEY")))
#     elif provider == "aws":
#         import boto3
#         client = boto3.client('comprehend')
#         return client.detect_sentiment
#     elif provider == "alibaba":
#         from alibabacloud_green20191206 import GreenClient
#         return GreenClient(endpoint='green.cn-hangzhou.aliyuncs.com',
#                             access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
#                             access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
#     elif provider == "perspective":
#         import requests
#         return lambda req: requests.post(
#             "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
#             params={"key": os.getenv("PERSPECTIVE_API_KEY")},
#             json=req).json()

__all__ = ["is_prompts_safe", "is_generated_safe"]
