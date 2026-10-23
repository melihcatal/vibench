# [LATER-STEP] platform_output_safety.py
# Check watsonx.ai model output for unsafe content using watsonx guardrails

import os
from ibm_watsonx_ai.hap.detection import ContentDetector, Mode
from typing import Dict


def check_safety(output: Dict[str, Any]) -> bool:
    """Run watsonx guardrails detection on generated text.

    Returns True if content is safe, False otherwise.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise ValueError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    detector = ContentDetector(api_key=api_key, project_id=project_id)
    # Guardrails supports multiple modes; using HAP (High Assurance Policy) here
    result = detector.detect(output["generated_text"], mode=Mode.Hap)
    # result.safe is a boolean indicating safety
    return result.safe
