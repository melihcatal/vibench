from typing import List, Dict, Any
from gemini_client import GeminiClient
import json


def image_summary(analysis_results: Dict[str, Any]) -> str:
    model = GeminiClient().get_model()

    prompt_parts = [
        "Summarize the following image analysis results in a concise paragraph:",
        json.dumps(analysis_results, indent=2),
    ]

    response = model.generate_content(prompt_parts)
    return response.text
