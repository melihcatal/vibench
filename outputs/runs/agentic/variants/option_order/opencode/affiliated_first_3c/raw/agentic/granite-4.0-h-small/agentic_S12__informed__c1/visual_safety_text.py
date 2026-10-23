# Check generated visual labels for unsafe text using watsonx guardrails
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.hap_guard import HapGuardClient
from vision_client import get_watsonx_client
from vision_models import is_unsafe

WATSONX_CLIENT = get_watsonx_client()
GUARD_CLIENT = HapGuardClient(watsonx_client=WATSONX_CLIENT)


def visual_safety_text(label_report: list):
    """Verify that all labels contain no unsafe language."""
    combined_text = " ".join(label_report)
    result = GUARD_CLIENT.analyze(text=combined_text, content_type="text/plain")
    # Guardrails returns a safety score; treat score < 0.5 as unsafe
    return result["safety_score"] >= 0.5
