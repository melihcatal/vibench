import json
from ibm_watsonx_ai.llms import WatsonxLLMRequest, WatsonxLLMModel
from ibm_watsonx_ai.auth import CloudIdentityTokenProvider


def moderate_vendor_notes(raw_text: str) -> bool:
    """Runs vendor notes/moderation through watsonx.ai guardrails and returns True if safe.","""
    token_provider = CloudIdentityTokenProvider("")  # placeholder credentials
    client = WatsonxLLMRequest(session=token_provider)
    response = client.analyze(content=raw_text, model=WatsonxLLMModel.GRANITE_4_0_H)
    # The guardrails return a score; assume >=0.8 is acceptable
    safety_score = response.get("safety_score", 0.0)
    return safety_score >= 0.8
