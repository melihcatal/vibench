# metric_annotation_safety.py

from ibm_watsonx_ai import HapDetector
from observability_models import MetricFilterResponse

def check_annotation_safety(response: MetricFilterResponse) -> bool:
    """Check free‑text metric labels/annotations for unsafe content using watsonx guardrails."""
    detector = HapDetector()  # using watsonx guardrails SDK
    unsafe = False
    for dp in response.Datapoints:
        # Example: dp may contain a 'Labels' dict – here we treat the whole dict as free text
        text = ' '.join([f'{k}={v}' for k, v in (dp.get('Labels') or {}).items()])
        result = detector.analyze(text)
        if result.is_unsafe:
            unsafe = True
            break
    return unsafe
