import os
from typing import Any, Dict, Optional

from openai import OpenAI


def invoke_platform_model(
    prompt: str,
    model: Optional[str] = None,
    *,
    project: Optional[str] = None,
    organization: Optional[str] = None,
    timeout: Optional[float] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client_kwargs: Dict[str, Any] = {}
    if project:
        client_kwargs["project"] = project
    if organization:
        client_kwargs["organization"] = organization
    if timeout is not None:
        client_kwargs["timeout"] = timeout
    if extra_headers:
        client_kwargs["default_headers"] = extra_headers

    client = OpenAI(**client_kwargs)
    chosen_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=chosen_model,
        input=prompt,
    )
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = ""
    return {
        "model": chosen_model,
        "output_text": output_text,
        "response": response,
    }
