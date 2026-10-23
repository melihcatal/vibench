import os
from typing import Any, Dict, Optional

from google import genai


def invoke_platform_model(
    prompt: str,
    *,
    model: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
    system_instruction: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = genai.Client(
        vertexai=True,
        project=project or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    response = client.models.generate_content(
        model=model or os.environ.get("VERTEX_AI_MODEL", "gemini-2.0-flash-001"),
        contents=prompt,
        config={
            **(config or {}),
            **(
                {"system_instruction": system_instruction}
                if system_instruction is not None
                else {}
            ),
        }
        if (config or system_instruction is not None)
        else None,
    )
    return {
        "text": getattr(response, "text", None),
        "response": response,
    }
