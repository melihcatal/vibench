import os
from typing import Any, Dict, Optional

from google import genai


def invoke_platform_model(
    prompt: str,
    *,
    project: Optional[str] = None,
    location: Optional[str] = None,
    model: Optional[str] = None,
    deployment: Optional[str] = None,
    inference_profile: Optional[str] = None,
    system_instruction: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1024,
) -> Dict[str, Any]:
    client = genai.Client(
        vertexai=True,
        project=project or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    resolved_model = model or deployment or inference_profile or os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash")
    response = client.models.generate_content(
        model=resolved_model,
        contents=prompt,
        config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "system_instruction": system_instruction,
        },
    )

    return {
        "provider": "google_vertex_ai",
        "model": resolved_model,
        "project": project or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        "location": location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "deployment": deployment,
        "inference_profile": inference_profile,
        "text": getattr(response, "text", None),
        "response": response,
    }
