import os
from typing import Iterable, List, Optional

from openai import OpenAI

from vision_client import build_openai_client

MODEL_ID = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def visual_safety_text(labels: Iterable[str], client: Optional[OpenAI] = None) -> str:
    client = client or build_openai_client()
    labels_text = "\n".join(f"- {label}" for label in labels)
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Assess whether visual labels imply unsafe, sensitive, or policy-relevant content."},
            {"role": "user", "content": f"Review these labels for safety concerns:\n{labels_text}"},
        ],
        temperature=0,
    )
    return response.output_text.strip()
