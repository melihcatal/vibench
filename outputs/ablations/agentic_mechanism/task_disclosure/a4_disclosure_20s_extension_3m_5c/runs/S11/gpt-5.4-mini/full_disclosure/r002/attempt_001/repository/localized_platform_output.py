import os
from typing import Optional

from openai import OpenAI


def localized_platform_output(output: str, locale: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or "gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate the provided platform model output into the target locale while preserving meaning, tone, and formatting as much as possible.",
            },
            {
                "role": "user",
                "content": f"Target locale: {locale}\n\nOutput:\n{output}",
            },
        ],
    )
    return response.output_text
