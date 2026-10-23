# visual_safety_text.py
from typing import List
from ibm_watsonx_ai.hap.detection import GuardrailsDetector
import os

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError('Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables')

def check_generated_text_safety(texts: List[str]) -> List[bool]:
    detector = GuardrailsDetector(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
    results = []
    for txt in texts:
        # Detect unsafe content (harassment, self-harm, etc.)
        resp = detector.detect(text=txt)
        # Simple pass/fail: any flagged category means unsafe
        safe = not any(item['severity'] > 0 for item in resp['flags'])
        results.append(safe)
    return results
