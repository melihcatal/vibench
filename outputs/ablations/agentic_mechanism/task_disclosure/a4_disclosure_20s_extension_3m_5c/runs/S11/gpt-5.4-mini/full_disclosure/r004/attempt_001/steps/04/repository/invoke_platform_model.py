import os
from typing import Any, Dict, List, Optional

from google import genai


def invoke_platform_model(
    prompt: str,
    *,
    model: str = "gemini-2.0-flash",
    project: Optional[str] = None,
    location: Optional[str] = None,
    generation_config: Optional[Dict[str, Any]] = None,
    safety_settings: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    client = genai.Client(
        vertexai=True,
        project=project or os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            **({"generation_config": generation_config} if generation_config else {}),
            **({"safety_settings": safety_settings} if safety_settings else {}),
        ),
    )
    return {
        "model": model,
        "text": getattr(response, "text", None),
        "response": response,
    }
