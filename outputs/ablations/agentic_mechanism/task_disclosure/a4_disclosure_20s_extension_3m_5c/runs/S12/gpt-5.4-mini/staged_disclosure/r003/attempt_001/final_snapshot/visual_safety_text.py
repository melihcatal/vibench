import os
from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def check_generated_visual_labels(labels: List[str]) -> Dict[str, Any]:
    prompt = (
        "Review these generated visual labels for unsafe text. "
        "Return JSON with keys unsafe, reasons, and safe_labels. Labels: "
        + ", ".join(labels)
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "output": response.output_text,
    }
