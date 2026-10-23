import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_visual_analysis(
    image_analysis: Dict[str, Any],
    image_url: Optional[str] = None,
) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Summarize the visual analysis results into a concise, clear paragraph. "
        "Focus on the main objects, scene, notable attributes, and any detected text or anomalies. "
        "If the analysis includes uncertainty, mention it briefly."
    )
    content: List[Dict[str, Any]] = [
        {"type": "text", "text": prompt + "\n\nAnalysis JSON:\n" + str(image_analysis)}
    ]
    if image_url:
        content.append({"type": "image_url", "image_url": {"url": image_url}})
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    return response.output_text
