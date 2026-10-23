import os
import mistralai
from typing import Dict, Any


def image_summary(analysis_results: Dict[str, Any]) -> str:
    client = mistralai.Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    labels_str = ", ".join(analysis_results.get("labels", []))
    description = analysis_results.get("description", "")
    detected_text = analysis_results.get("detected_text", "")
    safety = analysis_results.get("safety", {})
    prompt = f"""Summarize the following image analysis results into a concise paragraph:

- Labels: {labels_str}
- Description: {description}
- Detected Text: {detected_text}
- Safety: {safety}

Focus on key visual elements and overall content."""
    response = client.chat.complete(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
