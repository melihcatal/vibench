import os
from typing import Any, Dict, List

from openai import OpenAI

_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def image_summary(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these visual analysis results into a concise paragraph for a product or accessibility workflow."
    response = client.responses.create(
        model=_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt + "\n\n" + str(analysis_results)},
                ],
            }
        ],
        temperature=0.3,
    )
    text = getattr(response, "output_text", "") or ""
    return {"summary": text.strip(), "raw_text": text}
