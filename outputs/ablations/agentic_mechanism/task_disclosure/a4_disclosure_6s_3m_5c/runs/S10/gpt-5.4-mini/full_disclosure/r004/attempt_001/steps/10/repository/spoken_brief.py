import os
from typing import Any, Dict, List, Optional

import openai


def generate_spoken_brief(model_output: str, model: str = "openai/gpt-5.4-mini", instructions: Optional[str] = None) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = instructions or "Turn the model output into a short, natural spoken brief suitable for reading aloud. Keep it concise and conversational."
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": model_output},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content or ""
