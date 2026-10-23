# [LATER-STEP] visual_safety_text.py
# Check generated visual labels (or descriptions) for unsafe or policy‑sensitive language using watsonx guardrails
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.hap import HAPDetector
from typing import List, Dict


def assess_label_safety(labels: List[str]) -> Dict[str, Any]:
    """Run HAP guardrail detection on a list of text labels/descriptions.

    Args:
        labels (List[str]): Labels or short text fragments to evaluate.
    Returns:
        Dict[str, Any]: Guardrail assessment JSON (scores, flag details).
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not (api_key and project_id):
        raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set")
    detector = HAPDetector(api_key=api_key, project_id=project_id)
    # Guardrails accept plain text; we join labels for assessment
    assessment = detector.analyze(text=" ".join(labels))
    return assessment.to_dict()


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 2:
        print("Usage: visual_safety_text.py <label1> [label2 ...]")
        sys.exit(1)
    labels = sys.argv[1:]
    print(json.dumps(assess_label_safety(labels), indent=2))
