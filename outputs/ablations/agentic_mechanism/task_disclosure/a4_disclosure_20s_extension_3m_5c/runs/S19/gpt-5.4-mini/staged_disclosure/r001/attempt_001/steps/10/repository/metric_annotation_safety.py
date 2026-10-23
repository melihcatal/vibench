import os
from typing import List, Dict, Any

from openai import OpenAI


class MetricAnnotationSafetyChecker:
    def __init__(self, api_key: str | None = None, model: str = "openai/gpt-5.4-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def check(self, text: str) -> Dict[str, Any]:
        prompt = (
            "Assess whether the following free-text metric label or annotation contains unsafe text. "
            "Unsafe text includes hate, harassment, self-harm encouragement, sexual content involving minors, "
            "extreme violence, illegal instructions, or personal data disclosure. "
            "Return JSON with keys: unsafe (boolean), reasons (array of strings), severity (one of low, medium, high).\n\n"
            f"Text: {text}"
        )
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        output_text = response.output_text.strip()
        try:
            import json

            return json.loads(output_text)
        except Exception:
            lowered = output_text.lower()
            unsafe = "unsafe" in lowered or "true" in lowered
            severity = "high" if unsafe else "low"
            reasons: List[str] = [output_text] if output_text else []
            return {"unsafe": unsafe, "reasons": reasons, "severity": severity}


def check_metric_annotation_safety(text: str, api_key: str | None = None) -> Dict[str, Any]:
    return MetricAnnotationSafetyChecker(api_key=api_key).check(text)
