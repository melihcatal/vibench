from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


def check_script_safety(script: str) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="omni-moderation-latest", input=script)
    result = response.output[0].content[0].text if response.output and response.output[0].content else "{}"
    return {"raw": result, "provider": "openai", "model": "omni-moderation-latest"}
