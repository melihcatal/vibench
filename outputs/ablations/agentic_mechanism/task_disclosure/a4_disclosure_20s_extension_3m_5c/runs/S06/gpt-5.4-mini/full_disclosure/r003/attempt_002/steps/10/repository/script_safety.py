import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def check_script_safety(script: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or os.getenv("OPENAI_SAFETY_MODEL", "gpt-5.4-mini"),
        input=[
            {
                "role": "system",
                "content": "You review narration scripts for unsafe content. Return only valid JSON with keys safe (boolean), categories (array of strings), and notes (string).",
            },
            {"role": "user", "content": script},
        ],
    )
    text = getattr(response, "output_text", None)
    if text is None:
        chunks: List[str] = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                piece = getattr(content, "text", None)
                if piece:
                    chunks.append(piece)
        text = "".join(chunks)
    return {"provider": "openai", "model": model or os.getenv("OPENAI_SAFETY_MODEL", "gpt-5.4-mini"), "raw": text}
