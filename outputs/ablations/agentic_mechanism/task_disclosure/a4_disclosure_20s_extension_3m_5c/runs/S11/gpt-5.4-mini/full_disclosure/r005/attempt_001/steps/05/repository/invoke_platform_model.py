import os
from typing import Any, Dict, Optional

from openai import OpenAI


def invoke_platform_model(prompt: str, model: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or os.environ.get("OPENAI_MODEL", "openai/gpt-5.4-mini"),
        input=prompt,
        **kwargs,
    )
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    output_text += text
    return {"output": output_text, "response": response}
