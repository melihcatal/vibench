from __future__ import annotations

from typing import Dict

from observability_client import text_generation_model
from observability_models import AnnotationSafetyRequest


def metric_annotation_safety(request: AnnotationSafetyRequest) -> Dict[str, object]:
    model = text_generation_model()
    prompt = f"Assess whether this metric annotation contains unsafe or disallowed text. Reply with SAFE or UNSAFE and a short reason: {request.text}"
    result = model.predict(prompt=prompt, temperature=0.0, max_output_tokens=64)
    text = getattr(result, 'text', str(result))
    unsafe = "UNSAFE" in text.upper()
    return {"unsafe": unsafe, "assessment": text}
