import os
from typing import Any, Dict, Optional

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def assess_payload_safety(text: str, context: Optional[str] = None) -> Dict[str, Any]:
    client = _client()
    prompt = "Assess whether the following decrypted text payload contains unsafe content such as secrets, credentials, malware instructions, exfiltration steps, abuse, or sensitive personal data. Return JSON with keys safe, risk_level, and reasons."
    if context:
        prompt += f" Context: {context}"
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    output_text = getattr(response, "output_text", "")
    return {"provider": "openai", "model": OPENAI_MODEL, "analysis": output_text}
