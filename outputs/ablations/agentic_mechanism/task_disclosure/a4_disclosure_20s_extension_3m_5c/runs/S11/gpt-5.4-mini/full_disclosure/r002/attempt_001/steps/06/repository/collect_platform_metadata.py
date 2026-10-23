from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class PlatformMetadataResult:
    output: str
    metadata: Dict[str, Any]


def collect_platform_metadata(prompt: str, model: str = "gpt-5.4-mini", api_key: Optional[str] = None) -> PlatformMetadataResult:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model=model, input=prompt)
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_parts = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    output_parts.append(text)
        output_text = "".join(output_parts)
    metadata = {
        "provider": "openai",
        "model": getattr(response, "model", model),
        "id": getattr(response, "id", None),
        "usage": response.usage.model_dump() if getattr(response, "usage", None) else None,
        "output_ids": [getattr(item, "id", None) for item in getattr(response, "output", []) or []],
    }
    return PlatformMetadataResult(output=output_text or "", metadata=metadata)
